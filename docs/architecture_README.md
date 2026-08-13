# Northstar Support Bot — System Architecture & Data Flow

This document details the system architecture, database schema, request flow, and API contracts for the Northstar Retail Support Deflection system.

---

## 1. High-Level Architecture Overview

```text
┌───────────┐      HTTP POST      ┌────────────────┐      SQL Query      ┌────────────────┐
│  Chat UI  │ ──────────────────> │ Django Backend │ ──────────────────> │ MySQL Database │
└───────────┘                     └───────┬────────┘                     └────────────────┘
                                           │
                                           │ Context + Prompt
                                           ▼
                                   ┌────────────────┐
                                   │ AI/LLM Engine  │
                                   └────────────────┘
```

* **User Query:** User submits a support query via the Chat UI.
* **Context Retrieval:** Django extracts the `order_id` and queries MySQL (`northstar_db`) for the complete customer, product, order status, and return context.
* **AI Generation:** Django forwards the raw database context along with the user's intent to the AI Model to generate a friendly, factual response.
* **Response:** Django returns the AI response back to the Chat UI.

---

## 2. Step-by-Step Request Flow

1. User sends a message containing an order reference (e.g., "Where is my order 1001?").
2. The AI/Automation engine parses the message, identifies the intent (`ORDER_STATUS` / `RETURN_REFUND`), and extracts integer `order_id = 1001`.
3. The system queries the Django API endpoint `GET /api/v1/orders/1001/`.
4. Django ORM fetches the linked records from MySQL (Customer, Product, Order, and pre-fetched Return list).
5. Django DRF returns a structured JSON payload (`200 OK`) with full nested order details.
6. The AI Model uses the structured JSON context to construct a natural-language answer to the user.

---

## 3. Database Schema (`northstar_db`)

### CUSTOMERS
* `customer_id` (PK) — Auto-incrementing integer
* `name` — String
* `email` — String
* `phone` — String

### PRODUCTS
* `product_id` (PK) — Auto-incrementing integer
* `name` — String
* `category` — String
* `size` — String
* `price` — Decimal
* `stock_quantity` — Integer

### ORDERS
* `order_id` (PK) — Integer (e.g., 1001, 1002)
* `customer_id` (FK) — Foreign key to CUSTOMERS
* `product_id` (FK) — Foreign key to PRODUCTS
* `quantity` — Integer
* `status` — String (`PROCESSING`, `SHIPPED`, `DELIVERED`, `CANCELLED`)
* `expected_delivery` — Date (`YYYY-MM-DD`)

### RETURNS
* `return_id` (PK) — Auto-incrementing integer
* `order_id` (FK) — Foreign key to ORDERS
* `reason` — Text
* `return_status` — String (`REQUESTED`, `APPROVED`, `REJECTED`, `COMPLETED`)
* `refund_status` — String (`PENDING`, `PROCESSED`, `REFUNDED`)
* `refund_amount` — Decimal

### Entity Relationships
* Customer → 1:N → Order
* Product → 1:N → Order
* Order → 1:N → Return (an order can have multiple return line items; serialized as a nested array)

---

## 4. API Endpoints

### Order Context Lookup

* **URL:** `GET /api/v1/orders/<order_id>/`
* **URL Parameter:** `order_id` (Integer, e.g., `1001`)

#### Success Response (`200 OK`)

```json
{
  "status": "success",
  "data": {
    "order_id": 1001,
    "customer": {
      "customer_id": 1,
      "name": "Jane Doe",
      "email": "jane@example.com",
      "phone": "+254700000001"
    },
    "product": {
      "product_id": 1,
      "name": "Wireless Headphones",
      "category": "Electronics",
      "size": "Standard",
      "price": "89.99",
      "stock_quantity": 50
    },
    "quantity": 1,
    "status": "SHIPPED",
    "expected_delivery": "2026-08-15",
    "returns": [
      {
        "return_id": 1,
        "reason": "Damaged packaging",
        "return_status": "REQUESTED",
        "refund_status": "PENDING",
        "refund_amount": "89.99"
      }
    ]
  }
}
```

#### Fallback / Error Response (`404 Not Found`)

```json
{
  "status": "error",
  "message": "Order with ID '9999' not found."
}
```

---

## 5. Implementation Status

- [x] MySQL schema created & migrated (`northstar_db`)
- [x] DRF serializers & nested context lookup endpoint (`/api/v1/orders/<order_id>/`) functional
- [x] Test seed data expanded (5 populated entries: Order IDs 1001 through 1005)
- [x] Endpoint tested and verified returning `200 OK`
- [ ] AI Lead integration to trigger context lookup on intent detection