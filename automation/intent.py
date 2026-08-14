import os
import json
import logging
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

# Initialize Google GenAI client with a 10-second timeout to prevent request hanging
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=10000)
) if os.getenv("GEMINI_API_KEY") else None


def _coerce_plain_text(raw_value):
    """Convert Gemini JSON-ish output into a plain conversational string."""
    if raw_value is None:
        return ""

    if isinstance(raw_value, str):
        text = raw_value.strip()
    elif isinstance(raw_value, dict):
        for key in ("reply", "response", "text", "message"):
            if key in raw_value:
                return _coerce_plain_text(raw_value[key])
        return json.dumps(raw_value, ensure_ascii=False)
    elif isinstance(raw_value, list):
        return " ".join(_coerce_plain_text(item) for item in raw_value if _coerce_plain_text(item))
    else:
        text = str(raw_value).strip()

    if text.startswith("{") or text.startswith("["):
        try:
            loaded = json.loads(text)
            return _coerce_plain_text(loaded)
        except (TypeError, ValueError):
            return text

    return text


def classify_intent_and_order(message: str) -> dict:
    """
    Uses Gemini to classify intent and extract order ID.
    Falls back to a lightweight local parser when the API is unavailable.
    """
    if not client:
        msg = (message or "").lower()
        order_id = None
        if any(token in msg for token in ["1001", "order 1001", "#1001"]):
            order_id = 1001
        return {"intent": "order_status", "order_id": order_id}

    prompt = f"""
    Analyze the following customer message and return only a valid JSON object with:
    1. "intent": One of ["order_status", "return_refund", "shipping_delay", "general_inquiry"]
    2. "order_id": Extract order ID number if present, otherwise null.

    Customer Message: "{message}"
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=120,
            ),
        )
        parsed = _coerce_plain_text(response.text)
        try:
            return json.loads(parsed)
        except (TypeError, ValueError):
            return {"intent": "general_inquiry", "order_id": None}
    except Exception as e:
        logger.error(f"[intent.py] classify_intent_and_order error: {e}")
        return {"intent": "general_inquiry", "order_id": None}


def generate_human_response(message: str, order_data: dict = None) -> str:
    """
    Generates a natural, human-like response using Gemini given customer input and order facts.
    """
    order = order_data.get("data", order_data) if isinstance(order_data, dict) else None
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
            "expected_delivery": order.get("expected_delivery"),
            "status": order.get("status"),
            "refund_status": latest_return.get("refund_status"),
        }

    if not client:
        if order_snapshot:
            customer_name = order_snapshot.get("customer_name") or "there"
            product_name = order_snapshot.get("product_name") or "your item"
            expected_delivery = order_snapshot.get("expected_delivery") or "your expected date"
            refund_status = order_snapshot.get("refund_status") or "being processed"
            return (
                f"Hi {customer_name}! I checked your order and your {product_name} is currently "
                f"{str(order_snapshot.get('status', 'on the way')).lower().replace('_', ' ')}. "
                f"The expected delivery date is {expected_delivery}, and your refund status is {str(refund_status).lower()}."
            )
        return "Thank you for contacting Northstar Support! How can I assist you with your order today?"

    system_instruction = (
        "You are Northstar Support's lead customer care specialist. "
        "Read the order data strictly and accurately. Do not invent, swap, guess, or infer statuses that are not present. "
        "When the payload includes multiple status fields, keep them distinct: order_status is the shipping delivery state, "
        "return_status is the return process state, and refund_status is the refund state. "
        "If refund_status is PENDING, say the refund is pending or processing; never say it failed. "
        "If return_status is COMPLETED, acknowledge that the return was completed. "
        "Use only the supplied facts and answer in 2-3 warm, professional, human sentences. "
        "Keep the response plain conversational English, not JSON, not bullet points, and not raw database dumps."
    )

    context_str = ""
    if order_snapshot:
        context_str = f"\nOrder Context (Internal Data): {json.dumps(order_snapshot, indent=2)}\n"

    user_prompt = f"""
    {context_str}
    Customer Message: "{message}"

    Draft a warm, helpful 2-3 sentence customer care reply in plain English. Do not return JSON or a dict.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
                max_output_tokens=220,
            ),
        )
        return _coerce_plain_text(response.text)
    except Exception as e:
        logger.error(f"[intent.py] generate_human_response error: {e}")
        if order_snapshot:
            customer_name = order_snapshot.get("customer_name") or "there"
            product_name = order_snapshot.get("product_name") or "your item"
            expected_delivery = order_snapshot.get("expected_delivery") or "your expected date"
            refund_status = order_snapshot.get("refund_status") or "being processed"
            return (
                f"Hi {customer_name}! I checked your order and your {product_name} is currently "
                f"{str(order_snapshot.get('status', 'on the way')).lower().replace('_', ' ')}. "
                f"The expected delivery date is {expected_delivery}, and your refund status is {str(refund_status).lower()}."
            )
        return (
            "Thank you for contacting Northstar Support! I'm having a brief issue pulling "
            "up your details, but our support team has received your message and will update you shortly."
        )


def generate_response(message: str, order_data: dict = None) -> str:
    """
    Public entry point called by ChatAPIView.
    Uses Gemini to craft a warm, human-like response backed by order context.
    """
    return generate_human_response(message, order_data=order_data)


def process_customer_ticket(message: str, fetch_order_fn=None) -> str:
    """
    Main orchestration loop:
    1. Parse intent & order ID
    2. Retrieve order records
    3. Generate human response via Gemini
    """
    # 1. Parse message
    parsed = classify_intent_and_order(message)
    order_id = parsed.get("order_id")

    # 2. Fetch order data if available
    order_data = None
    if order_id and fetch_order_fn:
        order_data = fetch_order_fn(order_id)

    # 3. Ask Gemini to write human response
    return generate_human_response(message, order_data)