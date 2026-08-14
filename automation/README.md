\# Northstar Support Chatbot — AI Automation



\## Overview



The `automation` component provides the AI-assisted customer-support logic for the Northstar Support Deflection MVP.



It processes customer messages, identifies the customer's intent, extracts an order ID when available, retrieves the relevant order information, and generates a human-friendly support response.



The automation focuses on the three repetitive support areas identified for the MVP:



\* Order-status enquiries

\* Return and refund enquiries

\* Stock or general support enquiries



It also includes handling for shipping or delivery delays.



\## Automation Flow



```text

Customer Message

&#x20;      ↓

Intent Classification

&#x20;      ↓

Order ID Extraction

&#x20;      ↓

Order Lookup

&#x20;      ↓

Intent-Aware Response Generation

&#x20;      ↓

Django API

&#x20;      ↓

Frontend Chatbot

```



\## Main Component



The primary automation module is:



```text

automation/intent.py

```



This module contains the main functions responsible for the AI workflow.



\### `classify\_intent\_and\_order()`



This function:



\* Sends the customer message to Gemini for classification.

\* Identifies the customer's support intent.

\* Extracts the numeric order ID when present.

\* Validates the returned intent.

\* Falls back to local classification if Gemini is unavailable or returns invalid data.



Supported intents are:



```text

order\_status

return\_refund

shipping\_delay

general\_inquiry

```



\### `generate\_human\_response()`



This function generates the customer-facing response using the available order information.



Relevant information includes:



\* Customer name

\* Order ID

\* Product name

\* Quantity

\* Order status

\* Expected delivery date

\* Return status

\* Refund status



The response instructions keep order status, return status, and refund status separate so that a return or refund question is not incorrectly answered using only shipping information.



\### `generate\_response()`



This is the public response-generation entry point used by the Django API layer.



\### `process\_customer\_ticket()`



This function provides the complete automation pipeline:



1\. Classify the customer message.

2\. Extract the order ID.

3\. Retrieve the order information.

4\. Generate an intent-aware customer response.



\## Supported Customer Requests



\### Order Status



Example:



```text

Track order 1001

```



Expected intent:



```text

order\_status

```



\### Return or Refund



Example:



```text

I want to return order 1001

```



Expected intent:



```text

return\_refund

```



\### Shipping Delay



Example:



```text

My delivery is late for order 1001

```



Expected intent:



```text

shipping\_delay

```



\### General Enquiry



Example:



```text

Hello, I need help

```



Expected intent:



```text

general\_inquiry

```



\## Order Data



The automation uses order information supplied by the Django backend.



The automation can work with:



\* Order ID

\* Customer information

\* Product information

\* Quantity

\* Order status

\* Expected delivery date

\* Return information

\* Refund information



Customer names and order details are retrieved dynamically from the order data.



They are not hard-coded into the customer response.



\## Gemini Integration



The automation uses the Google Gemini API through the Google GenAI Python SDK.



The Gemini API key is loaded from the environment variable:



```text

GEMINI\_API\_KEY

```



The API key must not be committed to GitHub.



The `.env` file is therefore kept outside version control.



\## Fallback Behaviour



The automation includes local fallback logic.



If Gemini:



\* is unavailable,

\* returns invalid JSON,

\* returns an invalid intent,

\* or encounters an API error,



the system can fall back to local intent classification and database-backed responses.



This prevents the chatbot from completely failing when the external AI service is temporarily unavailable.



\## Gemini API Quota



During development, the Gemini API may return:



```text

429 RESOURCE\_EXHAUSTED

```



This means the configured Gemini API project has reached its available request quota.



This is an external API limitation and does not by itself indicate a failure in the Northstar application.



The automation therefore includes fallback handling so that the core support workflow can continue when Gemini is unavailable.



\## Frontend and Backend Integration



The frontend does not need to communicate directly with Gemini.



The general architecture is:



```text

Browser Chat UI

&#x20;     ↓

Django Chat API

&#x20;     ↓

Automation Layer

&#x20;     ↓

Gemini + Local Fallback

&#x20;     ↓

Order Database

&#x20;     ↓

Customer Response

&#x20;     ↓

Browser Chat UI

```



The frontend is responsible for:



\* collecting the customer's message,

\* displaying the chatbot response,

\* displaying relevant order information.



The backend automation is responsible for:



\* understanding the customer request,

\* classifying intent,

\* extracting the order ID,

\* retrieving order information,

\* generating the support response.



\## Testing



\### Python Syntax Check



Run:



```powershell

python -m py\_compile .\\automation\\intent.py

```



\### Local Intent Classification Test



Run:



```powershell

python manage.py shell -c "from automation.intent import \_local\_classification; print(\_local\_classification('Track order 1001')); print(\_local\_classification('I want to return order 1001')); print(\_local\_classification('My delivery is late for order 1001')); print(\_local\_classification('Hello, I need help'))"

```



Expected results:



```text

{'intent': 'order\_status', 'order\_id': 1001}

{'intent': 'return\_refund', 'order\_id': 1001}

{'intent': 'shipping\_delay', 'order\_id': 1001}

{'intent': 'general\_inquiry', 'order\_id': None}

```



\### Django Test Suite



Run:



```powershell

python manage.py test

```



\### Git Validation



Run:



```powershell

git diff --check

```



\## Development Branch



The automation work is developed on:



```text

feature/ai-automation

```



The recommended integration workflow is:



```text

feature/ai-automation

&#x20;       ↓

Testing

&#x20;       ↓

Documentation

&#x20;       ↓

Commit

&#x20;       ↓

Push

&#x20;       ↓

Pull Request

&#x20;       ↓

Team Review

&#x20;       ↓

Merge into main

```



The feature branch should be reviewed before being merged into the team's main branch.



\## Current Status



The AI automation component includes:



\* Gemini-based intent classification

\* Order ID extraction

\* Local fallback classification

\* Intent-aware response generation

\* Order-data integration

\* Return/refund handling

\* Shipping-delay handling

\* Gemini API error handling

\* Frontend/backend integration support

\* Automated validation and testing



\## Contribution



The AI automation component provides the intelligence layer of the Northstar Support Deflection MVP.



It connects customer messages with intent classification, order retrieval, and customer-friendly responses while maintaining a local fallback path to improve reliability when the external AI service is unavailable.
