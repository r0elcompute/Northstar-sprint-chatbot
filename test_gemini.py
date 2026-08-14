import os
from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("GEMINI_API_KEY is not set.")
        return

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents='Return exactly this JSON and nothing else: {"intent":"order_status","order_id":1001}',
    )

    print("RAW RESPONSE:")
    print(repr(response.text))


if __name__ == "__main__":
    main()