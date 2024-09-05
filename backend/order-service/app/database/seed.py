from app.database.database import SessionLocal
from app.models import Customer


def seed_customers():
    db = SessionLocal()
    try:
        customers = [
            Customer(id=1, name="Customer 1"),
            Customer(id=2, name="Customer 2"),
            Customer(id=3, name="Customer 3")
        ]

        db.add_all(customers)
        db.commit()

        print("Customers added successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()