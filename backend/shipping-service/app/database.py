from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.app_config import AppConfig

Base = declarative_base()

engine = create_engine(AppConfig.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_database():
    Base.metadata.create_all(bind=engine)
