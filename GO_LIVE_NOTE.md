# Go-Live Readiness Note: Northstar Support Deflection MVP

**Client:** Northstar Retail Co.
**Team:** Titans
**System Status:** MVP Live / Ready for Staging Evaluation

---

## 1. What Works Today (Verified in Code)

- **Two supported ticket types, fully working end-to-end:** Order Status and Returns/Refunds. A customer message like "Where is my order 1001?" or "I want to return order 1002" is classified, matched to real order data in the database, and answered automatically.
- **Order/return lookup:** The system extracts an order ID from the customer's message, retrieves the customer, product, order status, expected delivery date, and any return/refund record from the MySQL database.
- **Clear fallback:** Questions outside these two areas get an honest "I can currently help with order status and returns/refunds" response rather than a guess or a hallucinated answer.
- **Two working API endpoints:** `POST /api/v1/chat/` (conversational entry point) and `GET /api/v1/orders/<order_id>/` (structured order lookup).
- **Frontend:** A customer-facing chat interface (`templates/index.html`) is connected to both endpoints and renders order/return status inline.

## 2. Important Clarification: Response Generation

Current live responses are **template-based, not AI-generated**. The system (`support/ai_automation.py`) matches keywords to determine intent, then fills in a fixed response template with real order data (e.g. *"Your order #1001 is currently shipped. Expected delivery date is 2026-08-09."*). This is accurate and reliable, but it is rule-based logic, not a language model writing the reply.

A more advanced module (`automation/intent.py`) has already been built separately — it calls Gemini for both intent classification and natural-language response generation, includes a local fallback if the API is unavailable, and supports two additional categories (`shipping_delay`, `general_inquiry`) beyond the two currently live. **This module exists and works in isolation but is not yet connected to the live chat endpoint.** Wiring it in is the clearest next step to both broaden category coverage and make replies feel more natural — see Section 4.

## 3. Known Limitations & Edge Cases

- Only Order Status and Returns/Refunds are live; shipping-delay and general questions get the fallback message rather than a tailored answer.
- Responses are template strings, so phrasing is consistent but not adaptive to how the customer phrased their question.
- The database is currently seeded with test data (order IDs 1001–1020) — not Northstar's real order records.
- Order ID extraction relies on finding a number in the message; unusually formatted order references may not be detected.

## 4. Recommended Next Steps Before Full Launch

1. Decide whether to launch with the current rule-based responses (proven, predictable) or complete the integration of the AI-powered `automation/intent.py` module (broader coverage, more natural replies, requires a valid `GEMINI_API_KEY` and additional testing).
2. Replace seeded test data with a real or realistic Northstar product/order data connection.
3. Confirm production database credentials and connection details are separate from the current development/test setup.
4. Assign someone on Northstar's side to monitor fallback responses in the first weeks, since anything outside the supported categories is deferred rather than answered.

## 5. Instructions for Northstar's Internal Team (Handover Guide)

1. **Environment setup:** Copy `.env.example` to `.env` and fill in your database credentials and `GEMINI_API_KEY` (required only if/when the AI-powered module in Section 2 is connected).
2. **Dependencies & migration:** Run `pip install -r requirements.txt`, then run Django migrations for a fresh instance.
3. **Current execution point:** Ticket handling logic lives in `support/ai_automation.py` (`generate_response`), called from `support/views.py`'s chat endpoint. The separate, not-yet-connected AI module is `automation/intent.py`.
4. **Seeding test data:** Run `python seed.py` for sample customers, products, orders, and returns.

## 6. Team

- Constance Mukenyi — Frontend/UX
- Christine Wanja — AI/Automation
- Fanuel Rodgers — Backend
- Rachael Hinga — Database
- Didymus Kiai — Integration, QA/Documentation

---
*Prepared by Team Titans as part of a collaborative sprint build.*
