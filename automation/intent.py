import os
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def understand_message(message):
    prompt = f"""
You are the AI intent detector for the Northstar customer support chatbot.

The chatbot currently supports three types of requests:

1. ORDER_STATUS
   Use this when the customer is asking about the status, location,
   delivery, or arrival of an order.

2. RETURNS_REFUNDS
   Use this when the customer wants to return an item, request a refund,
   or ask about an existing return or refund.

3. UNSUPPORTED
   Use this when the customer's request is not related to order status
   or returns/refunds.

Read the customer's message and identify:
- intent
- order_id, if one is provided

Important rules:

- If the customer asks about order status and provides an order number,
  classify it as ORDER_STATUS and extract the order number.

- If the customer asks about order status but does not provide an order
  number, classify it as ORDER_STATUS and use UNKNOWN for the order_id.

- If the customer asks for a return or refund and provides an order number,
  classify it as RETURNS_REFUNDS and extract the order number.

- If the customer asks for a return or refund but does not provide an
  order number, classify it as RETURNS_REFUNDS and use UNKNOWN for the
  order_id.

- If the customer's request is unrelated to order status or
  returns/refunds, classify it as UNSUPPORTED and use UNKNOWN for the
  order_id.

Return your answer in this exact format:

intent: ORDER_STATUS, RETURNS_REFUNDS, or UNSUPPORTED
order_id: the order number or UNKNOWN

Customer message:
{message}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


message = input("Customer: ")

result = understand_message(message)

print("\nAI result:")
print(result)