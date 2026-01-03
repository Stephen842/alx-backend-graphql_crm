from crm.models import Customer, Product, Order
from django.utils import timezone
from decimal import Decimal


def run():
    # Clear existing data (safe for re-runs)
    Order.objects.all().delete()
    Customer.objects.all().delete()
    Product.objects.all().delete()

    # ---- Customers ----
    alice = Customer.objects.create(
        name="Alice",
        email="alice@example.com",
        phone="+1234567890"
    )

    bob = Customer.objects.create(
        name="Bob",
        email="bob@example.com",
        phone="123-456-7890"
    )

    carol = Customer.objects.create(
        name="Carol",
        email="carol@example.com"
    )

    dave = Customer.objects.create(
        name="Dave",
        email="dave@example.com",
        phone="+1987654321"
    )

    eve = Customer.objects.create(
        name="Eve",
        email="eve@example.com",
        phone="321-654-0987"
    )

    # ---- Products ----
    laptop = Product.objects.create(
        name="Laptop",
        price=Decimal("999.99"),
        stock=10
    )

    phone = Product.objects.create(
        name="Phone",
        price=Decimal("499.99"),
        stock=20
    )

    headset = Product.objects.create(
        name="Headset",
        price=Decimal("79.99"),
        stock=50
    )

    keyboard = Product.objects.create(
        name="Keyboard",
        price=Decimal("49.99"),
        stock=30
    )

    mouse = Product.objects.create(
        name="Mouse",
        price=Decimal("29.99"),
        stock=40
    )

    monitor = Product.objects.create(
        name="Monitor",
        price=Decimal("199.99"),
        stock=15
    )

    # ---- Orders ----
    order_1 = Order.objects.create(
        customer=alice,
        order_date=timezone.now(),
        total_amount=laptop.price + headset.price
    )
    order_1.products.set([laptop, headset])

    order_2 = Order.objects.create(
        customer=bob,
        order_date=timezone.now(),
        total_amount=phone.price + keyboard.price
    )
    order_2.products.set([phone, keyboard])

    order_3 = Order.objects.create(
        customer=carol,
        order_date=timezone.now(),
        total_amount=mouse.price + monitor.price
    )
    order_3.products.set([mouse, monitor])

    order_4 = Order.objects.create(
        customer=dave,
        order_date=timezone.now(),
        total_amount=laptop.price + phone.price + headset.price
    )
    order_4.products.set([laptop, phone, headset])

    order_5 = Order.objects.create(
        customer=eve,
        order_date=timezone.now(),
        total_amount=keyboard.price + mouse.price
    )
    order_5.products.set([keyboard, mouse])

    print("Database seeded successfully!")
