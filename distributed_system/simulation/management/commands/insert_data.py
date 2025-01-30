import threading
from django.core.management.base import BaseCommand
from simulation.models import User, Product, Order


class Command(BaseCommand):
    help = "Insert data into multiple databases concurrently"

    def handle(self, *args, **options):
        # Define data for Users, Products, and Orders
        user_data = [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
            {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
            {"id": 4, "name": "David", "email": "david@example.com"},
            {"id": 5, "name": "Eve", "email": "eve@example.com"},
            {"id": 6, "name": "Frank", "email": "frank@example.com"},
            {"id": 7, "name": "Grace", "email": "grace@example.com"},
            {"id": 8, "name": "Alice", "email": "alice@example.com"},
            {"id": 9, "name": "Henry", "email": "henry@example.com"},
            {"id": 10, "name": "Jane", "email": "jane@example.com"},
        ]
        product_data = [
            {"id": 1, "name": "Laptop", "price": 1000.00},
            {"id": 2, "name": "Smartphone", "price": 700.00},
            {"id": 3, "name": "Headphones", "price": 150.00},
            {"id": 4, "name": "Monitor", "price": 300.00},
            {"id": 5, "name": "Keyboard", "price": 50.00},
            {"id": 6, "name": "Mouse", "price": 30.00},
            {"id": 7, "name": "Laptop", "price": 1000.00},
            {"id": 8, "name": "Smartwatch", "price": 250.00},
            {"id": 9, "name": "Gaming Chair", "price": 500.00},
            {"id": 10, "name": "Earbuds", "price": 20.00},
        ]
        order_data = [
            {"id": 1, "user_id": 1, "product_id": 1, "quantity": 2},
            {"id": 2, "user_id": 2, "product_id": 2, "quantity": 1},
            {"id": 3, "user_id": 3, "product_id": 3, "quantity": 5},
            {"id": 4, "user_id": 4, "product_id": 4, "quantity": 1},
            {"id": 5, "user_id": 5, "product_id": 5, "quantity": 3},
            {"id": 6, "user_id": 6, "product_id": 6, "quantity": 4},
            {"id": 7, "user_id": 7, "product_id": 7, "quantity": 2},
            {"id": 8, "user_id": 8, "product_id": 8, "quantity": 1},
            {"id": 9, "user_id": 9, "product_id": 9, "quantity": 1},
            {"id": 10, "user_id": 10, "product_id": 10, "quantity": 2},
        ]

        # Define threading functions for data insertion
        def insert_users():
            for data in user_data:
                try:
                    User.objects.using('users').create(**data)
                    print(f"User inserted: {data}")
                except Exception as e:
                    print(f"Error inserting user {data}: {e}")

        def insert_products():
            for data in product_data:
                try:
                    Product.objects.using('products').create(**data)
                    print(f"Product inserted: {data}")
                except Exception as e:
                    print(f"Error inserting product {data}: {e}")

        def insert_orders():
            for data in order_data:
                try:
                    Order.objects.using('orders').create(**data)
                    print(f"Order inserted: {data}")
                except Exception as e:
                    print(f"Error inserting order {data}: {e}")

        # Start threads for concurrent insertion
        threads = [
            threading.Thread(target=insert_users),
            threading.Thread(target=insert_products),
            threading.Thread(target=insert_orders),
        ]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        self.stdout.write(self.style.SUCCESS('Data insertion completed!'))
