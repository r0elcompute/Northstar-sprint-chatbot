import requests


def detect_intent(message):
    """
    Identify the type of support request from the customer's message.
    """

    message = message.lower()

    if any(word in message for word in [
        "where is my order",
        "order status",
        "track my order",
        "tracking",
        "delivery",
        "shipped"
    ]):
        return "ORDER_STATUS"

    if any(word in message for word in [
        "return",
        "refund",
        "money back",
        "send back"
    ]):
        return "RETURN_REFUND"

    return "UNKNOWN"


def get_order_information(order_id):
    """
    Retrieve order information from the Northstar Django API.
    """

    url = f"http://127.0.0.1:8000/api/v1/orders/{order_id}/"

    response = requests.get(url, timeout=5)

    if response.status_code == 200:
        return response.json()

    return None


def generate_response(message, order_id=None):
    """
    Route the customer's request and generate an automated response.
    """

    intent = detect_intent(message)

    if intent == "UNKNOWN":
        return {
            "intent": intent,
            "response": (
                "I'm sorry, I can currently help with "
                "order status and returns/refunds."
            )
        }

    if not order_id:
        return {
            "intent": intent,
            "response": "Sure! Please provide your order number."
        }

    order_data = get_order_information(order_id)

    if not order_data:
        return {
            "intent": intent,
            "response": (
                f"I couldn't find order #{order_id}. "
                "Please check the order number and try again."
            )
        }

    order = order_data["data"]

    if intent == "ORDER_STATUS":
        return {
            "intent": intent,
            "response": (
                f"Your order #{order['order_id']} is currently "
                f"{order['status'].lower().replace('_', ' ')}. "
                f"The expected delivery date is "
                f"{order['expected_delivery']}."
            )
        }

    if intent == "RETURN_REFUND":
        returns = order.get("returns", [])

        if not returns:
            return {
                "intent": intent,
                "response": (
                    f"I couldn't find a return or refund record "
                    f"for order #{order['order_id']}."
                )
            }

        latest_return = returns[-1]

        return {
            "intent": intent,
            "response": (
                f"For order #{order['order_id']}, your return is "
                f"{latest_return['return_status'].lower()}. "
                f"Your refund status is "
                f"{latest_return['refund_status'].lower()}."
            )
        }