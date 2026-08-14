import os
import random
import django
from datetime import date, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from support.models import Customer, Product, Order, Return

def seed_database():
    print("Clearing existing data...")
    Return.objects.all().delete()
    Order.objects.all().delete()
    Product.objects.all().delete()
    Customer.objects.all().delete()

    print("Seeding new test data...")

    # 1. Seed 20 Customers
    first_names = ["Jane", "John", "Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Hannah",
                   "Ian", "Julia", "Kevin", "Laura", "Michael", "Nora", "Oscar", "Pamela", "Quinn", "Rachel"]
    last_names = ["Doe", "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez",
                  "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson"]

    customers = []
    for i in range(20):
        customer = Customer.objects.create(
            name=f"{first_names[i]} {last_names[i]}",
            email=f"{first_names[i].lower()}.{last_names[i].lower()}@example.com",
            phone=f"+2547{random.randint(10000000, 99999999)}"
        )
        customers.append(customer)

    # 2. Seed 20 Products
    product_catalogue = [
        ("Wireless Headphones", "Electronics", "Standard", 89.99),
        ("Ergonomic Gaming Mouse", "Electronics", "Medium", 45.50),
        ("Cotton Crewneck T-Shirt", "Apparel", "L", 19.99),
        ("Stainless Steel Water Bottle", "Accessories", "750ml", 24.99),
        ("Mechanical Keyboard", "Electronics", "Full-Size", 110.00),
        ("Ultra-wide Monitor", "Electronics", "27-inch", 299.99),
        ("Noise Cancelling Earbuds", "Electronics", "Small", 129.50),
        ("Denim Jacket", "Apparel", "M", 65.00),
        ("Slim Fit Chinos", "Apparel", "32x32", 42.00),
        ("Running Shoes", "Apparel", "42 EU", 85.00),
        ("Leather Wallet", "Accessories", "Compact", 35.00),
        ("Canvas Backpack", "Accessories", "20L", 49.99),
        ("Smartwatch Band", "Accessories", "22mm", 15.00),
        ("USB-C Docking Station", "Electronics", "Standard", 75.00),
        ("HD Webcam", "Electronics", "1080p", 55.00),
        ("Desk Mat", "Accessories", "XL", 22.50),
        ("Hooded Sweatshirt", "Apparel", "XL", 38.00),
        ("Bluetooth Speaker", "Electronics", "Portable", 48.00),
        ("Polarized Sunglasses", "Accessories", "One Size", 29.99),
        ("Fitness Tracker", "Electronics", "Standard", 60.00),
    ]

    products = []
    for name, cat, size, price in product_catalogue:
        product = Product.objects.create(
            name=name,
            category=cat,
            size=size,
            price=price,
            stock_quantity=random.randint(5, 150)
        )
        products.append(product)

    # 3. Seed 20 Orders (Order IDs 1001 to 1020)
    order_statuses = ["PROCESSING", "SHIPPED", "DELIVERED", "CANCELLED"]
    reasons = ["Damaged packaging", "Wrong item delivered", "Defective product", "Changed mind", "Item arrived late", "Size did not fit"]
    today = date.today()

    for i in range(20):
        order_id = 1001 + i
        customer = customers[i]
        product = products[i]
        quantity = random.randint(1, 3)
        status = random.choice(order_statuses)

        # --- Rule 1: Delivery dates strictly tied to status ---
        if status == "CANCELLED":
            expected_delivery = None
        elif status in ("PROCESSING", "SHIPPED"):
            expected_delivery = today + timedelta(days=random.randint(1, 7))
        else:  # DELIVERED
            expected_delivery = today - timedelta(days=random.randint(1, 14))

        order = Order.objects.create(
            order_id=order_id,
            customer=customer,
            product=product,
            quantity=quantity,
            status=status,
            expected_delivery=expected_delivery
        )

        refund_amt = round(float(product.price) * quantity, 2)

        # --- Rule 2: Return & refund relationships strictly tied to status ---
        if status == "CANCELLED":
            # Cancelled orders always get an automatic completed refund
            Return.objects.create(
                order=order,
                reason="Order cancelled before shipping",
                return_status="COMPLETED",
                refund_status="PROCESSED",
                refund_amount=refund_amt
            )

        elif status == "DELIVERED":
            # 50% chance a delivered order has a return
            if random.random() < 0.5:
                return_status = random.choice(["REQUESTED", "APPROVED", "REJECTED", "COMPLETED"])

                if return_status == "COMPLETED":
                    refund_status = random.choice(["PROCESSED", "PENDING"])
                elif return_status == "REJECTED":
                    refund_status = random.choice(["FAILED", "NOT_APPLICABLE"])
                else:  # REQUESTED or APPROVED
                    refund_status = "PENDING"

                Return.objects.create(
                    order=order,
                    reason=random.choice(reasons),
                    return_status=return_status,
                    refund_status=refund_status,
                    refund_amount=refund_amt
                )

        # PROCESSING and SHIPPED orders NEVER get Return/refund records
        # (no else branch needed — simply skipped)

    print("Database successfully seeded with realistic order, return, and refund workflows!")

if __name__ == '__main__':
    seed_database()