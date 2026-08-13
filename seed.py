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

    print("Seeding new test data (20 records per table)...")

    # 1. Seed 20 Customers
    first_names = ["Jane", "John", "Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Hannah", 
                   "Ian", "Julia", "Kevin", "Laura", "Michael", "Nora", "Oscar", "Pamela", "Quinn", "Rachel"]
    last_names = ["Doe", "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez",
                  "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson"]

    customers = []
    for i in range(20):
        fname = first_names[i]
        lname = last_names[i]
        customer = Customer.objects.create(
            name=f"{fname} {lname}",
            email=f"{fname.lower()}.{lname.lower()}@example.com",
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
    today = date.today()

    orders = []
    for i in range(20):
        order_id = 1001 + i
        customer = customers[i]  # Map 1:1 or use random.choice(customers)
        product = random.choice(products)
        quantity = random.randint(1, 3)
        status = random.choice(order_statuses)
        
        # Delivery dates relative to today
        delivery_offset = random.randint(-5, 10)
        expected_delivery = today + timedelta(days=delivery_offset)

        order = Order.objects.create(
            order_id=order_id,
            customer=customer,
            product=product,
            quantity=quantity,
            status=status,
            expected_delivery=expected_delivery
        )
        orders.append(order)

    # 4. Seed 20 Return entries (linked across the 20 orders)
    reasons = [
        "Damaged packaging", "Wrong item delivered", "Defective product", 
        "Changed mind", "Item arrived late", "Size did not fit"
    ]
    return_statuses = ["REQUESTED", "APPROVED", "REJECTED", "COMPLETED"]
    refund_statuses = ["PENDING", "PROCESSED", "REFUNDED", "FAILED"]

    # Pick 20 orders (with replacement or shuffle) to assign return requests
    sampled_orders = random.choices(orders, k=20)

    for order in sampled_orders:
        refund_amt = round(float(order.product.price) * order.quantity, 2)
        Return.objects.create(
            order=order,
            reason=random.choice(reasons),
            return_status=random.choice(return_statuses),
            refund_status=random.choice(refund_statuses),
            refund_amount=refund_amt
        )

    print("Database successfully seeded with 20 records per table!")

if __name__ == '__main__':
    seed_database()