from django.test import SimpleTestCase

from support.ai_automation import classify_intent_and_order, generate_response


class AiAutomationApiTests(SimpleTestCase):
    def test_classify_intent_and_order_exists(self):
        result = classify_intent_and_order("Where is my order 1234?")
        self.assertIn("intent", result)
        self.assertIn("order_id", result)

    def test_generate_response_accepts_order_data(self):
        response = generate_response(
            "Where is my order?",
            order_data={
                "data": {
                    "order_id": 1234,
                    "status": "SHIPPED",
                    "expected_delivery": "2026-08-20",
                    "returns": [],
                }
            },
        )
        self.assertIn("intent", response)
        self.assertIn("response", response)
