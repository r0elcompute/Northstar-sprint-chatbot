import os
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def understand_message(message):
    prompt = f"""
You are the AI intent detector for the Northstar customer support chatbot.

The chatbot currently supports only two types of requests:

1. ORDER_STATUS
2. RETURNS_REFUNDS

Read the customer's message and identify:
- intent
- order_id, if one is provided

Return your answer in this exact format:

intent: ORDER_STATUS or RETURNS_REFUNDS
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