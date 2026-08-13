import os
import django

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

    # 1. Create 5 Customers
    customers_data = [
        {"name": "Jane Doe", "email": "jane@example.com", "phone": "+254700000001"},
        {"name": "John Smith", "email": "john.smith@example.com", "phone": "+254700000002"},
        {"name": "Alice Johnson", "email": "alice.j@example.com", "phone": "+254700000003"},
        {"name": "Bob Williams", "email": "bob.w@example.com", "phone": "+254700000004"},
        {"name": "Charlie Brown", "email": "charlie.b@example.com", "phone": "+254700000005"},
    ]
    customers = [Customer.objects.create(**c) for c in customers_data]

    # 2. Create 5 Products
    products_data = [
        {"name": "Wireless Headphones", "category": "Electronics", "size": "Standard", "price": 89.99, "stock_quantity": 50},
        {"name": "Ergonomic Gaming Mouse", "category": "Electronics", "size": "Medium", "price": 45.50, "stock_quantity": 120},
        {"name": "Cotton Crewneck T-Shirt", "category": "Apparel", "size": "L", "price": 19.99, "stock_quantity": 200},
        {"name": "Stainless Steel Water Bottle", "category": "Accessories", "size": "750ml", "price": 24.99, "stock_quantity": 80},
        {"name": "Mechanical Keyboard", "category": "Electronics", "size": "Full-Size", "price": 110.00, "stock_quantity": 35},
    ]
    products = [Product.objects.create(**p) for p in products_data]

    # 3. Create 5 Orders (Order IDs 1001 to 1005)
    orders_data = [
        {"order_id": 1001, "customer": customers[0], "product": products[0], "quantity": 1, "status": "SHIPPED", "expected_delivery": "2026-08-15"},
        {"order_id": 1002, "customer": customers[1], "product": products[1], "quantity": 2, "status": "DELIVERED", "expected_delivery": "2026-08-10"},
        {"order_id": 1003, "customer": customers[2], "product": products[2], "quantity": 3, "status": "PROCESSING", "expected_delivery": "2026-08-18"},
        {"order_id": 1004, "customer": customers[3], "product": products[3], "quantity": 1, "status": "SHIPPED", "expected_delivery": "2026-08-14"},
        {"order_id": 1005, "customer": customers[4], "product": products[4], "quantity": 1, "status": "DELIVERED", "expected_delivery": "2026-08-08"},
    ]
    orders = [Order.objects.create(**o) for o in orders_data]

    # 4. Create 3 Return entries linked to specific orders
    returns_data = [
        {"order": orders[0], "reason": "Damaged packaging", "return_status": "REQUESTED", "refund_status": "PENDING", "refund_amount": 89.99},
        {"order": orders[1], "reason": "Wrong item delivered", "return_status": "APPROVED", "refund_status": "PROCESSED", "refund_amount": 91.00},
        {"order": orders[4], "reason": "Defective key switch", "return_status": "COMPLETED", "refund_status": "REFUNDED", "refund_amount": 110.00},
    ]
    for r in returns_data:
        Return.objects.create(**r)

    print("Database successfully seeded with 5 entries per main table!")

if __name__ == '__main__':
    seed_database()