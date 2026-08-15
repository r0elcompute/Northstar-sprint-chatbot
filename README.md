# Northstar Support Deflection MVP

A support chatbot for Northstar Retail Co. that gives customers instant answers on **Order Status** and **Returns/Refunds** — deflecting the most common, repetitive support tickets away from human agents.

Built by Team Titans as part of the PLP Software Engineering program.

---

## How it works

1. A customer sends a message through the chat interface (e.g. "Where's my order 1001?").
2. The Django backend detects intent and extracts any order ID mentioned.
3. It looks up the relevant order, customer, product, and return data in the MySQL database.
4. That data plus the original question is sent to Gemini (AI), which generates a natural-language reply.
5. The reply — and an order status card, if applicable — is shown back in the chat.

Questions outside these two supported areas get a clear fallback message rather than a guess.

---

## Project structure

- **`templates/index.html`** — the customer-facing chat frontend (single-file HTML/CSS/JS)
- **`support/`** — Django app: models, API views, serializers for orders, customers, products, and returns
- **`automation/`** — AI intent detection and Gemini integration
- **`config/`** — Django project settings and URL routing
- **`seed.py`** / **`init_db.py`** — populate the database with test data
- **`docs/`** — deeper documentation on each part of the system (see below)

---

## Documentation

- [`docs/Backend_README.md`](docs/Backend_README.md) — backend setup, environment variables, running the Django server locally
- [`docs/frontend-README.md`](docs/frontend-README.md) — running the chat frontend, pointing it at a backend, known limitations
- [`docs/architecture_README.md`](docs/architecture_README.md) — system architecture overview
- [`docs/chatbot-decision-flow.md`](docs/chatbot-decision-flow.md) — the chatbot's conversation/decision flow
- [`docs/ai-automation-foundation.md`](docs/ai-automation-foundation.md) — intents, example questions, and fallback design
- [`automation/README.md`](automation/README.md) — AI/automation implementation notes
- [`TEAM_CHARTER.md`](TEAM_CHARTER.md) — how the team works: communication, workflow, roles, and definition of done

---

## Quick start

1. Clone the repo and set up a Python virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Add a `.env` file with your database and Gemini API credentials (see `docs/Backend_README.md` for the required variables).
4. Run migrations: `python manage.py migrate`
5. (Optional) Seed test data: `python seed.py`
6. Start the server: `python manage.py runserver`
7. Open `templates/index.html` in a browser — it defaults to `http://127.0.0.1:8000/api/v1`, adjustable via the ⚙ settings panel in the chat header.

---

## Team

See [`TEAM_CHARTER.md`](TEAM_CHARTER.md) for full team roles, workflow, and working agreement.
