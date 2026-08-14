# Northstar Support — Frontend

Customer-facing chat interface for the Northstar Support Deflection MVP. Handles two supported ticket types: **Order Status** and **Returns/Refunds**, plus a fallback for anything unsupported.

## What it is

A single self-contained file (`index.html`) — HTML, CSS, and JavaScript in one place. No build step, no dependencies, no npm install. Just open it in a browser.

## Running it

1. Make sure the backend is running locally at `http://127.0.0.1:8000` (see the backend setup guide in `docs/Backend_README.md`).
2. Open `frontend/index.html` directly in a browser (double-click it, or drag it into a browser window).
3. Try the quick-start chips ("Track order 1001", "Start a return") or type your own message.

That's it — no server needed to host the frontend itself for local testing.

## Pointing it at a different backend

Click the ⚙ icon in the top-right of the chat header. It opens a settings panel where you can change the **API base URL** (defaults to `http://127.0.0.1:8000/api/v1`). Useful if the backend is running on a different port, a teammate's machine, or a deployed URL.

The dot next to the ⚙ icon shows connection status: green means it can reach the backend, red means it can't (check the API base URL first if it's red).

## How it talks to the backend

- `POST /api/v1/chat/` — sends the user's message (and an order ID if one was mentioned) and gets back a natural-language reply.
- `GET /api/v1/orders/<order_id>/` — used to render the order/return status card under the chat reply, when the message includes an order ID.

## UI states covered

- Loading (animated typing indicator while waiting on the backend)
- Success (chat reply + order status card, when applicable)
- Order not found (404 from the orders endpoint)
- Unsupported question (client-side fallback message, no backend call needed)
- Server/connection error

## Known limitations

- Order ID detection is a simple regex match (looks for a 3–6 digit number in the message) — not full NLP intent parsing. It works for the MVP's numeric order IDs but won't handle more complex phrasing.
- "Supported topic" detection for the fallback message is also a lightweight keyword check on the frontend, done before calling the backend at all. It's a first pass to keep the UI responsive; the AI backend does its own (more capable) intent detection on `/chat/` regardless.
- No conversation history is saved between page reloads — each open of `index.html` starts a fresh chat.
- Tested against the seeded order ID range (1001–1020).
