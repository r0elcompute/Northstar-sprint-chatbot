
**Project Name:** Northstar Sprint Chatbot
**Target Release Date.**August 2026
**Branch:**Feature/integration +QA/Documentation'
**Status** Ready for development 

## What We Built

This is a support deflection MVP for Northstar Retail Co. It handles two of the three required ticket types — **Order Status** and **Returns & Refunds** — through a working chat interface backed by a real MySQL database. When a customer asks something like "Where is ORD-1001?", the system pulls the order, customer, and product details from the database, hands that context to the AI, and sends back a plain-language answer.

## How It Works

The flow is simple: Chat UI talks to a Django backend, which talks to a MySQL database. When a user sends a message, Django extracts the order ID, looks up the order, customer, and return info, then passes all of that plus the question to the AI. The AI writes a natural reply, and Django sends it back to the chat.

**Main endpoint:** `POST /api/v1/chat/` — takes a message like "Where is ORD-1001?" and returns a natural-language status update.

**Supporting endpoint:** `GET /api/v1/orders/<order_id>/` — returns full order, customer, and product details as structured data.

## What's in the Database

We built four core tables: **Customers**, **Products**, **Orders**, and **Returns**, linked by customer and product IDs. A customer can have many orders, and each order can have its own return record. We seeded the database with realistic test data — 20 customers, 20 products across Electronics, Apparel, and Accessories, and 20 orders in varying states (Processing, Shipped, Delivered, Cancelled), plus a handful of returns with different statuses (Requested, Approved, Completed) and refund amounts.

## Who Worked on What

- **Christine (AI/Automation):** built the chatbot's intent logic, conversation flow, and fallback handling for unsupported questions.
- **Constance (Frontend):** built the customer-facing chat interface and connected it to the backend.
- **Rachel (Database):** designed the schema, built the MySQL database, and seeded it with realistic sample data.
- **Didymus (Integration, QA & Documentation):** merged team branches for testing, reviewed each part against the live database, and wrote this readiness note.

## What Works Today

- Order status lookups return accurate, real-time data from the database.
- Return and refund records are stored and retrievable per order.
- The API returns clean, structured JSON that the AI can turn into a natural reply.

## What Still Needs Attention

- Stock availability checks are not yet wired into the chatbot's supported flows.
- End-to-end testing across all three ticket types is still in progress.
- Production credentials for the live MySQL instance haven't been finalized — the current setup uses test data only.

## What Northstar's Team Needs To Do Before Going Live

1. Swap in production database credentials (the current instance is seeded with sample/test data).
2. Confirm the AI provider and API key to be used long-term — this is currently marked TBD in our architecture.
3. Review the seeded data structure against Northstar's real product catalog and customer records before connecting to live data.
4. Assign someone to monitor fallback responses in the first weeks, since the bot defers to a human for anything outside order status and returns.

---
*Prepared by the Northstar Sprint Chatbot team as part of a 1-week collaborative build.*
