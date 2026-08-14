# Chatbot Decision Flow

## Purpose

This document describes how the chatbot should handle the two supported customer-support intents: Order Status and Returns/Refunds.

## Overall Flow

1. Customer sends a message.
2. The chatbot receives the message.
3. The AI/automation layer identifies the customer's intent.
4. If the intent is ORDER_STATUS, the system follows the Order Status flow.
5. If the intent is RETURNS_REFUNDS, the system follows the Returns/Refunds flow.
6. If the intent cannot be identified, the chatbot provides a fallback response.
7. The system returns an appropriate response to the customer.

## ORDER_STATUS Flow

Customer message
→ Identify intent
→ ORDER_STATUS
→ Request or identify the required order information
→ Send the request to the backend
→ Retrieve available order information
→ Return the order status to the customer

Example:

Customer:
"Where is my order?"

Intent:
ORDER_STATUS

Expected action:
Retrieve the relevant order information and provide the available status to the customer.

## RETURNS_REFUNDS Flow

Customer message
→ Identify intent
→ RETURNS_REFUNDS
→ Identify the relevant return/refund request
→ Send the request to the backend
→ Retrieve the relevant information
→ Return appropriate guidance or status to the customer

Example:

Customer:
"I want to return my order."

Intent:
RETURNS_REFUNDS

Expected action:
Provide the appropriate return information or initiate the relevant return process.

## Fallback Flow

Customer message
→ Identify intent
→ Intent is not supported or cannot be identified
→ FALLBACK

Example response:

"I'm currently able to help with order status and returns/refunds. Could you please rephrase your question?"

## Phase 1 Goal

The decision flow provides a clear blueprint for implementing and testing the chatbot automation in the next phase.
