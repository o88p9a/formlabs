
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



