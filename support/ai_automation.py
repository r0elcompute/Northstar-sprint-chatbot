import re


def detect_intent(message):
    message = message.lower()

    order_keywords = [
        "where is my order",
        "where is my package",
        "order status",
        "track my order",
        "tracking",
        "delivery",
        "shipped",
        "package",
        "parcel",
    ]

    return_keywords = [
        "return",
        "refund",
        "money back",
        "send back",
        "exchange",
    ]

    if any(keyword in message for keyword in order_keywords):
        return "ORDER_STATUS"

    if any(keyword in message for keyword in return_keywords):
        return "RETURN_REFUND"

    return "UNKNOWN"


def classify_intent_and_order(message):
    """Return a normalized intent and any order number found in the message."""
    intent = detect_intent(message)
    order_id = None

    match = re.search(r"\b(\d{1,10})\b", message or "")
    if match:
        order_id = int(match.group(1))

    if intent == "UNKNOWN":
        return {"intent": "general_inquiry", "order_id": order_id}

    return {"intent": intent, "order_id": order_id}


def get_order_information(order_id):
    """
    Retrieve order information directly from the database.

    This used to make an HTTP request back to this same Django server
    (http://127.0.0.1:8000/api/v1/orders/<id>/). On a single-threaded dev
    server that call blocks on itself: the in-flight request handling the
    chat message can't also serve the second connection, so it hangs until
    the 5s timeout and surfaces as a 504. Since this code already lives in
    the same app as the Order model, querying it directly removes the
    network round-trip (and the deadlock) entirely.
    """
    from .models import Order
    from .serializers import OrderSerializer

    try:
        order = (
            Order.objects
            .select_related('customer', 'product')
            .prefetch_related('returns')
            .get(order_id=order_id)
        )
    except Order.DoesNotExist:
        return None

    return {"status": "success", "data": OrderSerializer(order).data}


def generate_response(message, order_data=None, order_id=None):
    """
    Route the customer's request and generate an automated response.
    Supports both the older order_id contract and the newer order_data contract.
    """

    intent = classify_intent_and_order(message).get("intent", detect_intent(message))
    order = None

    if order_data is not None:
        order = order_data.get("data", order_data)
    elif order_id is not None:
        order_data = get_order_information(order_id)
        order = order_data.get("data", order_data) if order_data else None

    if intent in ("UNKNOWN", "general_inquiry"):
        return {
            "intent": intent,
            "response": (
                "I'm sorry, I can currently help with "
                "order status and returns/refunds."
            ),
        }

    if not order:
        return {
            "intent": intent,
            "response": "Sure! Please provide your order number.",
        }

    order_id_value = order.get("order_id") or order_id

    if intent == "ORDER_STATUS":
        return {
            "intent": intent,
            "response": (
                f"Your order #{order_id_value} is currently "
                f"{str(order.get('status', 'unknown')).lower().replace('_', ' ')}. "
                f"The expected delivery date is "
                f"{order.get('expected_delivery', 'not available')}."
            ),
        }

    if intent == "RETURN_REFUND":
        returns = order.get("returns", [])

        if not returns:
            return {
                "intent": intent,
                "response": (
                    f"I couldn't find a return or refund record "
                    f"for order #{order_id_value}."
                ),
            }

        latest_return = returns[-1]

        return {
            "intent": intent,
            "response": (
                f"For order #{order_id_value}, your return is "
                f"{str(latest_return.get('return_status', 'unknown')).lower()}. "
                f"Your refund status is "
                f"{str(latest_return.get('refund_status', 'unknown')).lower()}."
            ),
        }

    return {
        "intent": intent,
        "response": "Thanks for reaching out. I can help with order updates and returns.",
    }