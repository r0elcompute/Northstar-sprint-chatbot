# AI Automation

This component handles the AI and automation layer of the Northstar Support Deflection MVP.

## Responsibilities

- Identify the customer's support intent.
- Extract relevant information such as an order ID.
- Request relevant information from the Django backend API.
- Receive structured JSON data.
- Use the available information to generate a customer-friendly response.
- Support the Order Status and Returns/Refunds flows.

## Current Phase

Phase 2 — Actual Automation

## Initial Goal

Convert a customer message into structured information containing:

- intent
- order_id, when available
