from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Batch(Base):
    __tablename__ = 'batches'

    id = Column(Integer, primary_key=True)
    sample_part_name = Column(String)
    material_id = Column(String)
    quantity = Column(Integer)
