# Chatbot Intent Test Cases

## Purpose

These test cases will be used to check whether the chatbot correctly identifies customer questions as Order Status, Returns/Refunds, or Unsupported.

## ORDER_STATUS

| # | Customer message | Expected intent |
|---|---|---|
| 1 | Where is my order? | ORDER_STATUS |
| 2 | Has my package shipped? | ORDER_STATUS |
| 3 | Can I track my order? | ORDER_STATUS |
| 4 | When will my order arrive? | ORDER_STATUS |
| 5 | What is the status of my delivery? | ORDER_STATUS |

## RETURNS_REFUNDS

| # | Customer message | Expected intent |
|---|---|---|
| 1 | How do I return an item? | RETURNS_REFUNDS |
| 2 | I want to return my order. | RETURNS_REFUNDS |
| 3 | Can I get a refund? | RETURNS_REFUNDS |
| 4 | When will I receive my refund? | RETURNS_REFUNDS |
| 5 | What is your return policy? | RETURNS_REFUNDS |

## UNSUPPORTED

| # | Customer message | Expected behavior |
|---|---|---|
| 1 | What is the weather today? | FALLBACK |
| 2 | Tell me a joke. | FALLBACK |
| 3 | I want to change my account password. | FALLBACK |

## Pass Condition

A test passes when the chatbot identifies the expected intent or provides the expected fallback response.
