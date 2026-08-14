# Northstar Support Chatbot — AI Automation

## Overview

The `automation` component provides the AI-assisted customer-support logic for the Northstar Support chatbot.

It processes customer messages, identifies the customer's intent, extracts an order ID when available, retrieves the relevant order information, and generates a human-friendly support response.

The automation is designed for the Northstar MVP use case, which focuses on:

* Order-status enquiries
* Return and refund enquiries
* Shipping or delivery delays
* General customer enquiries

## Automation Flow

The automation follows this general flow:

```text
Customer Message
       ↓
Intent Classification
       ↓
Order ID Extraction
       ↓
Order Lookup
       ↓
Intent-Aware Response Generation
       ↓
Django API
       ↓
Frontend Chatbot
```

## Main Component

The primary automation module is:

```text
automation/intent.py
```

It contains the main functions responsible for the AI workflow.

### `classify_intent_and_order()`

This function:

* Sends the customer message to Gemini for classification.
* Identifies the customer's intent.
* Extracts the numeric order ID when present.
* Validates the returned intent.
* Falls back to local classification if Gemini is unavailable or returns invalid data.

Supported intents are:

```text
order_status
return_refund
shipping_delay
general_inquiry
```

### `generate_human_response()`

This function generates the customer-facing response using:

* Customer information
* Product information
* Order status
* Expected delivery date
* Return status
* Refund status
* The classified customer intent

The response instructions prevent the AI from confusing order status, return status, and refund status.

### `generate_response()`

This is the public response-generation entry point used by the Django API layer.

### `process_customer_ticket()`

This function provides the complete automation pipeline:

1. Classify the customer message.
2. Extract the order ID.
3. Retrieve the order information.
4. Generate an intent-aware response.

## Supported Customer Requests

### Order Status

Example:

```text
Track order 1001
```

Expected intent:

```text
order_status
```

### Return or Refund

Example:

```text
I want to return order 1001
```

Expected intent:

```text
return_refund
```

### Shipping Delay

Example:

```text
My delivery is late for order 1001
```

Expected intent:

```text
shipping_delay
```

### General Enquiry

Example:

```text
Hello, I need help
```

Expected intent:

```text
general_inquiry
```

## Order Information

The automation uses order information supplied by the Django backend.

Relevant information includes:

* Order ID
* Customer name
* Product name
* Quantity
* Order status
* Expected delivery date
* Return status
* Refund status

Customer information is retrieved dynamically from the order record.

Customer names are therefore **not hard-coded** into the automation.

## Gemini Integration

The automation uses the Google Gemini API through the Google GenAI Python SDK.

The Gemini API key is loaded from the environment:

```text
GEMINI_API_KEY
```

The API key should not be committed to GitHub.

The `.env` file is therefore kept outside version control.

## Fallback Behaviour

The automation includes local fallback logic.

If Gemini:

* is unavailable,
* returns invalid JSON,
* returns an invalid intent,
* or encounters an API error,

the system can use local intent classification and database-backed responses instead of completely failing the chatbot.

This makes the MVP more resilient to external AI service failures.

## API Quota Consideration

During development, Gemini may return:

```text
429 RESOURCE_EXHAUSTED
```

This indicates that the configured Gemini API project has reached its available request quota.

This is an external API limitation and does not necessarily indicate a failure in the Northstar application.

The automation therefore includes fallback handling so that core support functionality can continue when the AI service is temporarily unavailable.

## Frontend Integration

The frontend communicates with the Django backend rather than calling Gemini directly.

The general architecture is:

```text
Browser Chat UI
      ↓
Django Chat API
      ↓
Automation Layer
      ↓
Gemini + Local Fallback
      ↓
Order Database
      ↓
Customer Response
      ↓
Browser Chat UI
```

The frontend is responsible for displaying the response and order information.

The backend automation is responsible for interpreting the customer request and producing the support response.

## Testing

Python syntax can be checked with:

```powershell
python -m py_compile .\automation\intent.py
```

Local intent classification can be tested with:

```powershell
python manage.py shell -c "from automation.intent import _local_classification; print(_local_classification('Track order 1001')); print(_local_classification('I want to return order 1001')); print(_local_classification('My delivery is late for order 1001')); print(_local_classification('Hello, I need help'))"
```

Expected results include:

```text
{'intent': 'order_status', 'order_id': 1001}
{'intent': 'return_refund', 'order_id': 1001}
{'intent': 'shipping_delay', 'order_id': 1001}
{'intent': 'general_inquiry', 'order_id': None}
```

The Django test suite can be run with:

```powershell
python manage.py test
```

Git whitespace errors can be checked with:

```powershell
git diff --check
```

## Git Workflow

The automation work is developed on:

```text
feature/ai-automation
```

The recommended workflow is:

```text
feature/ai-automation
        ↓
Testing
        ↓
README/documentation
        ↓
Commit
        ↓
Push
        ↓
Pull Request
        ↓
Team Review
        ↓
Merge into main
```

The automation branch should not be merged into `main` until the final tests and documentation are complete and the team is ready to integrate the feature.

## Contribution

The automation component contributes the AI-assisted support workflow for the Northstar MVP by connecting customer messages with intent classification, order retrieval, and human-friendly responses while maintaining a local fallback for resilience.
