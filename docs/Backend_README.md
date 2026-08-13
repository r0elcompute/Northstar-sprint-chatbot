# Northstar Retail – Support API Setup & Endpoints Guide

This document outlines the setup, local testing steps, and API endpoint details for the backend support module.

---

## Key Links & Local URLs

* **Base Server URL:** `http://127.0.0.1:8000/`
* **API Base Endpoint:** `http://127.0.0.1:8000/api/v1/`
* **Order Lookup URL Format:** `http://127.0.0.1:8000/api/v1/orders/<order_id>/`
* **Example Live Test Link:** [http://127.0.0.1:8000/api/v1/orders/1001/](http://127.0.0.1:8000/api/v1/orders/1001/)

---

## Step-by-Step Local Setup Guide

Follow these steps in order to run the project locally on your machine.

### Step 1: Clone & Navigate to Project

```powershell
git clone git@github.com:r0elcompute/Northstar-sprint-chatbot.git
cd project-folder-name
```

### Step 2: Set Up Virtual Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate on Windows (PowerShell)
.\venv\Scripts\activate

# Activate on Linux / macOS
source venv/bin/activate
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Environment Variables Setup (`.env`)

Create a file named `.env` in the root folder (where `manage.py` lives) and paste the following configuration:

```
SECRET_KEY=django-insecure-key-for-local-dev
DEBUG=True
DB_NAME=northstar_db
DB_USER=root
DB_PASSWORD=your_local_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
```

### Step 5: Initialize MySQL Database & Run Migrations

1. Ensure your local MySQL server is running on `127.0.0.1:3306`.
2. Create the target database in MySQL:

```sql
CREATE DATABASE northstar_db;
```

3. Apply Django database schema migrations:

```powershell
python manage.py migrate
```

### Step 6: Seed Dummy Data

Populate the database with test customers, products, orders, and returns:

```powershell
python seed.py
```

### Step 7: Launch Development Server

```powershell
python manage.py runserver
```

The server will now be listening at `http://127.0.0.1:8000/`.

---

## API Endpoint Reference

### Order Details Lookup

* **Endpoint:** `/api/v1/orders/<order_id>/`
* **Method:** `GET`
* **URL Parameter:** `order_id` (Integer, e.g., `1001`)

#### Sample Request

```http
GET http://127.0.0.1:8000/api/v1/orders/1001/
```

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
      "phone": "+254700000000"
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

#### Error Response (`404 Not Found`)

```json
{
  "status": "error",
  "message": "Order with ID '9999' not found."
}
```

---

## File Architecture

* `config/` — Global Django project configuration & root URL router (`urls.py`).
* `support/` — Core app containing models, serializers, views, and app routing (`urls.py`).
* `manage.py` — Django CLI tool.
* `seed.py` — Database population script.
* `requirements.txt` — Project dependencies file.
* `.gitignore` — Version control tracking exclusions.