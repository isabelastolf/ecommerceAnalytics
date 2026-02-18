import random
from datetime import datetime, timedelta

from app.core.database import SessionLocal, engine, Base
from app.models.customer import Customer
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.payment import Payment


def create_tables():
    Base.metadata.create_all(bind=engine)


def random_date():
    return datetime.now() - timedelta(days=random.randint(1, 365))


def seed():
    db = SessionLocal()

    # Customers
    customers = []
    for i in range(300):
        email = f"user{i}@mail.com"
        if i % 10 == 0:
            email = "duplicate@mail.com"

        customer = Customer(
            name=f"Customer {i}",
            email=email,
            created_at=random_date(),
        )
        db.add(customer)
        customers.append(customer)

    db.commit()

    # Products
    products = []
    for i in range(50):
        product = Product(
            name=f"Product {i}",
            price=random.randint(10, 500),
            stock=random.choice([10, 5, -3, 0]),
        )
        db.add(product)
        products.append(product)

    db.commit()

    # Orders
    orders = []
    for i in range(2000):
        total = random.randint(100, 1000)
        if i % 7 == 0:
            total += 50  # erro proposital

        order = Order(
            customer_id=random.randint(1, 50),
            total=total,
            status=random.choice(["paid", "pending", "cancelled"]),
            created_at=random_date(),
        )
        db.add(order)
        orders.append(order)

    db.commit()

    # Order Items
    for order in orders:
        for _ in range(random.randint(1, 3)):
            product = random.choice(products)
            item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=random.randint(1, 10),
                price=product.price,
            )
            db.add(item)

    db.commit()

    # Payments
    for order in orders[:1850]:
        payment = Payment(
            order_id=order.id,
            amount=order.total,
            status=random.choice(["paid", "failed", "pending"]),
        )
        db.add(payment)

    db.commit()
    db.close()


if __name__ == "__main__":
    create_tables()
    seed()
    print("Database seeded successfully.")
