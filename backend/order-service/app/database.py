
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.app_config import AppConfig

engine = create_engine(AppConfig.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_database():
    Base.metadata.create_all(bind=engine)
    seed_customers()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def seed_customers():
    from app.models import Customer
    db = SessionLocal()
    try:
        customers = [
            {"id": 1, "name": "Customer 1"},
            {"id": 2, "name": "Customer 2"},
            {"id": 3, "name": "Customer 3"}
        ]

        for customer_data in customers:
            existing_customer = db.query(Customer).filter_by(id=customer_data["id"]).first()

            if not existing_customer:
                new_customer = Customer(id=customer_data["id"], name=customer_data["name"])
                db.add(new_customer)
            else:
                print(f"Customer with id {customer_data['id']} already exists.")

        db.commit()
        print("Customers added successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()



