# AI & Automation Foundation

## Project

Northstar sprint Support Deflection MVP

## Purpose

The AI and automation component will help reduce repetitive customer-support work by identifying customer questions and directing them to the correct support flow.

## Supported Intents

### 1. ORDER_STATUS

The customer wants information about an existing order, such as its status, shipment, tracking, or expected delivery.

Example questions:
 -  Where is my order?
 - Has my order shipped?
 - Can I track my package?
 - When will my order arrive?

### 2. RETURNS_REFUNDS

The customer wants information about returning an item or receiving a refund.

Example questions:
- How do I return an item?
- I want to return my order.
- Can I get a refund?
- When will I receive my refund?

## Unsupported Questions

If the chatbot cannot identify the question as one of the supported intents, it should provide a fallback response rather than pretending to know the answer.

Example:

"I'm currently able to help with order status and returns/refunds. Could you please rephrase your question?"

## Phase 1 Goal

Create a clear foundation for the chatbot's intent handling before implementing the actual automation logic.
