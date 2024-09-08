from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from app.database import Base

class Status(PyEnum):
    PENDING = "pending"
    PRINTING = "printing"
    PRINTED = "printed"


class PrintOrder(Base):
    __tablename__ = 'print_orders'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    customer_name = Column(String)
    status = Column(Enum(Status), default=Status.PENDING)

    items = relationship("PrintOrderItem", back_populates="order")


class PrintOrderItem(Base):
    __tablename__ = 'print_order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('print_orders.id'))
    sample_part_id = Column(Integer)
    material_id = Column(Integer)
    quantity = Column(Integer)
    status = Column(Enum(Status), default=Status.PENDING)

    order = relationship("PrintOrder", back_populates="items")
