import os
import json
import logging
import re

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Gemini client
# ---------------------------------------------------------

client = (
    genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
        http_options=types.HttpOptions(timeout=30000),
    )
    if os.getenv("GEMINI_API_KEY")
    else None
)


# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------

def _coerce_plain_text(raw_value):
    """Convert Gemini output into plain text."""

    if raw_value is None:
        return ""

    if isinstance(raw_value, str):
        return raw_value.strip()

    if isinstance(raw_value, dict):
        for key in ("reply", "response", "text", "message"):
            if key in raw_value:
                return _coerce_plain_text(raw_value[key])

        return json.dumps(raw_value, ensure_ascii=False)

    if isinstance(raw_value, list):
        return " ".join(
            _coerce_plain_text(item)
            for item in raw_value
            if _coerce_plain_text(item)
        )

    return str(raw_value).strip()


# ---------------------------------------------------------
# Local classification fallback
# ---------------------------------------------------------

def _local_classification(message):
    """
    Classify common Northstar support messages locally.

    This protects the chatbot when Gemini is unavailable,
    times out, or the API quota has been reached.
    """

    msg = (message or "").lower()

    order_id = None

    # Extract the first numeric order ID.
    match = re.search(r"\b(\d{1,10})\b", msg)

    if match:
        order_id = int(match.group(1))

    # Return/refund must be checked first.
    if any(
        phrase in msg
        for phrase in [
            "return",
            "refund",
            "money back",
            "send back",
            "exchange",
        ]
    ):
        intent = "return_refund"

    # Shipping delay must come before general delivery/order-status.
    elif any(
        phrase in msg
        for phrase in [
            "shipping delay",
            "shipping is late",
            "shipping late",
            "delivery delay",
            "delivery is late",
            "delivery late",
            "late delivery",
            "delayed delivery",
            "my delivery is late",
            "my delivery is delayed",
            "package is late",
            "package is delayed",
            "parcel is late",
            "parcel is delayed",
            "hasn't arrived",
            "has not arrived",
            "still waiting",
            "where is my package",
        ]
    ):
        intent = "shipping_delay"

    # Normal order-status requests.
    elif any(
        phrase in msg
        for phrase in [
            "track",
            "tracking",
            "order status",
            "where is my order",
            "check my order",
            "check order",
            "status of my order",
        ]
    ):
        intent = "order_status"

    else:
        intent = "general_inquiry"

    return {
        "intent": intent,
        "order_id": order_id,
    }


# ---------------------------------------------------------
# Intent classification
# ---------------------------------------------------------

def classify_intent_and_order(message: str) -> dict:
    """
    Classify the customer's intent and extract an order ID.

    Gemini is used first.

    If Gemini fails, returns invalid JSON, times out,
    or the API quota is exhausted, the local classifier
    is used instead.
    """

    # If no Gemini API key exists, use local classification.
    if not client:
        fallback = _local_classification(message)
        print("LOCAL CLASSIFICATION:", fallback)
        return fallback

    prompt = f"""
Classify the following Northstar customer support message.

Return ONLY one valid JSON object.
Do not explain anything.
Do not use markdown.
Do not add any text before or after the JSON.

The JSON must contain exactly these two fields:

{{
  "intent": "order_status",
  "order_id": 1001
}}

Allowed intent values are ONLY:

- "order_status"
- "return_refund"
- "shipping_delay"
- "general_inquiry"

Rules:

- Use "order_status" when the customer wants to track or check the current status of an order.
- Use "return_refund" when the customer wants to return an item, asks about a refund, asks for money back, or asks about an exchange.
- Use "shipping_delay" when the customer says the delivery or shipping is late, delayed, or has not arrived.
- Use "general_inquiry" for other questions.
- Extract the numeric order ID when one is present.
- If no order ID is present, use null.

Customer message:
{message}
"""

    parsed_text = ""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0,
                max_output_tokens=256,
                response_mime_type="application/json",
            ),
        )

        raw_response = response.text or ""
        parsed_text = _coerce_plain_text(raw_response)

        print("GEMINI RAW RESPONSE:", repr(parsed_text))

        parsed = json.loads(parsed_text)

        if not isinstance(parsed, dict):
            raise ValueError(
                "Gemini returned a non-object JSON response."
            )

        intent = parsed.get("intent")
        order_id = parsed.get("order_id")

        allowed_intents = {
            "order_status",
            "return_refund",
            "shipping_delay",
            "general_inquiry",
        }

        if intent not in allowed_intents:
            raise ValueError(
                f"Invalid intent returned by Gemini: {intent}"
            )

        if order_id is not None:
            order_id = int(order_id)

        return {
            "intent": intent,
            "order_id": order_id,
        }

    except Exception as e:
        logger.error(
            f"[intent.py] Gemini classification failed: {e}"
        )

        fallback = _local_classification(message)

        print("LOCAL FALLBACK:", fallback)

        return fallback


# ---------------------------------------------------------
# AI response generation
# ---------------------------------------------------------

def generate_human_response(
    message: str,
    order_data: dict = None,
    intent: str = "general_inquiry",
) -> str:
    """
    Generate a human-friendly customer-support response.

    The intent is explicitly supplied so a return/refund
    request cannot accidentally receive only an order-status
    response.
    """

    order = (
        order_data.get("data", order_data)
        if isinstance(order_data, dict)
        else None
    )

    order_snapshot = {}

    if isinstance(order, dict):

        customer = order.get("customer") or {}
        product = order.get("product") or {}
        returns = order.get("returns") or []

        latest_return = returns[-1] if returns else {}

        order_snapshot = {
            "order_id": order.get("order_id"),
            "customer_name": customer.get("name"),
            "product_name": product.get("name"),
            "quantity": order.get("quantity"),
            "status": order.get("status"),
            "expected_delivery": order.get("expected_delivery"),
            "return_status": latest_return.get("return_status"),
            "refund_status": latest_return.get("refund_status"),
        }

    # -----------------------------------------------------
    # Local response fallback
    # -----------------------------------------------------

    if not client:

        # RETURN / REFUND
        if intent == "return_refund":

            if not order_snapshot:
                return (
                    "Please provide your order number so I can check "
                    "your return or refund information."
                )

            return_status = order_snapshot.get("return_status")
            refund_status = order_snapshot.get("refund_status")

            if not return_status and not refund_status:
                return (
                    f"I checked order #{order_snapshot.get('order_id')}, "
                    "but I couldn't find an existing return or refund record. "
                    "If you'd like to start a return, I can help with the next steps."
                )

            return (
                f"I checked order #{order_snapshot.get('order_id')}. "
                f"Your return status is "
                f"{return_status or 'not available'}, and your refund status is "
                f"{refund_status or 'not available'}."
            )

        # SHIPPING DELAY
        if intent == "shipping_delay":

            if not order_snapshot:
                return (
                    "Please provide your order number so I can check "
                    "the delivery status."
                )

            customer_name = order_snapshot.get("customer_name") or "there"
            status = (
                str(order_snapshot.get("status", "unknown"))
                .lower()
                .replace("_", " ")
            )
            expected_delivery = (
                order_snapshot.get("expected_delivery")
                or "not available"
            )

            return (
                f"Hi {customer_name}! I checked order "
                f"#{order_snapshot.get('order_id')}, and its current status "
                f"is {status}. The expected delivery date is "
                f"{expected_delivery}."
            )

        # ORDER STATUS
        if intent == "order_status":

            if not order_snapshot:
                return (
                    "Please provide your order number so I can check "
                    "your order status."
                )

            customer_name = order_snapshot.get("customer_name") or "there"

            status = (
                str(order_snapshot.get("status", "unknown"))
                .lower()
                .replace("_", " ")
            )

            expected_delivery = (
                order_snapshot.get("expected_delivery")
                or "not available"
            )

            return (
                f"Hi {customer_name}! I checked order "
                f"#{order_snapshot.get('order_id')} and your "
                f"{order_snapshot.get('product_name') or 'item'} is currently "
                f"{status}. The expected delivery date is "
                f"{expected_delivery}."
            )

        # GENERAL INQUIRY
        return (
            "Thank you for contacting Northstar Support! "
            "I can help with order status and returns or refunds. "
            "What would you like to know?"
        )

    # -----------------------------------------------------
    # Gemini response generation
    # -----------------------------------------------------

    system_instruction = (
        "You are Northstar Support's lead customer care specialist. "

        "The customer's intent is explicitly provided. "
        "You MUST answer according to that intent. "

        "If the intent is order_status, discuss the order's "
        "shipping or delivery status. "

        "If the intent is return_refund, discuss the return or "
        "refund information. Do NOT answer a return/refund "
        "question with only the shipping status. "

        "If the intent is shipping_delay, discuss the delivery "
        "or shipping timing. "

        "Use only the supplied order facts. "
        "Never invent a return, refund, status, date, product, "
        "quantity, or customer detail. "

        "Keep order status, return status, and refund status distinct. "

        "If there is no return or refund record, clearly explain "
        "that no return or refund record was found. "

        "Use the customer's actual name from the order data when available. "
        "Do not assume the customer's name is Jane. "

        "Respond in 2-3 warm, professional sentences. "
        "Use plain conversational English. "
        "Do not return JSON, bullet points, or database dumps."
    )

    context_str = ""

    if order_snapshot:
        context_str = (
            "\nOrder Context:\n"
            f"{json.dumps(order_snapshot, indent=2)}\n"
        )

    user_prompt = f"""
Customer Intent:
{intent}

{context_str}

Customer Message:
{message}

Write the appropriate Northstar customer-support response.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
                max_output_tokens=220,
            ),
        )

        return _coerce_plain_text(response.text)

    except Exception as e:

        logger.error(
            f"[intent.py] generate_human_response error: {e}"
        )

        # Safe response if Gemini response generation fails.
        if intent == "return_refund":

            if order_snapshot:
                return (
                    f"I checked order #{order_snapshot.get('order_id')}, "
                    "but I'm having trouble generating the full return/refund "
                    "response right now. Please try again shortly."
                )

            return (
                "I'm having trouble checking the return or refund information "
                "right now. Please provide your order number and try again."
            )

        if intent == "shipping_delay":

            if order_snapshot:
                return (
                    f"I checked order #{order_snapshot.get('order_id')}, "
                    "but I'm having trouble generating the full delivery "
                    "response right now. Please try again shortly."
                )

            return (
                "I'm having trouble checking the delivery information "
                "right now. Please provide your order number and try again."
            )

        if intent == "order_status":

            if order_snapshot:
                return (
                    f"I checked order #{order_snapshot.get('order_id')}, "
                    "but I'm having trouble generating the full order-status "
                    "response right now. Please try again shortly."
                )

            return (
                "I'm having trouble checking the order status right now. "
                "Please provide your order number and try again."
            )

        return (
            "Thank you for contacting Northstar Support! "
            "I'm having a brief issue processing your request. "
            "Please try again shortly."
        )


# ---------------------------------------------------------
# Public response function
# ---------------------------------------------------------

def generate_response(
    message: str,
    order_data: dict = None,
    intent: str = None,
) -> str:
    """
    Public entry point used by ChatAPIView.
    """

    if intent is None:
        parsed = classify_intent_and_order(message)
        intent = parsed.get(
            "intent",
            "general_inquiry",
        )

    return generate_human_response(
        message,
        order_data=order_data,
        intent=intent,
    )


# ---------------------------------------------------------
# Full automation pipeline
# ---------------------------------------------------------

def process_customer_ticket(
    message: str,
    fetch_order_fn=None,
) -> str:
    """
    Full Northstar automation pipeline:

    1. Classify customer intent.
    2. Extract order ID.
    3. Retrieve order information.
    4. Generate an intent-aware response.
    """

    parsed = classify_intent_and_order(message)

    intent = parsed.get(
        "intent",
        "general_inquiry",
    )

    order_id = parsed.get("order_id")

    order_data = None

    if order_id and fetch_order_fn:
        order_data = fetch_order_fn(order_id)

    return generate_human_response(
        message,
        order_data=order_data,
        intent=intent,
    )
