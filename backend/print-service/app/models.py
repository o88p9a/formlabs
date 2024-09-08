from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class PrintOrder(Base):
    __tablename__ = 'print_orders'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    customer_name = Column(String)
    status = Column(String, default='pending')  # pending, printing, completed

    items = relationship("PrintOrderItem", back_populates="order")


class PrintOrderItem(Base):
    __tablename__ = 'print_order_items'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('print_orders.id'))
    sample_part_id = Column(Integer)
    material_id = Column(Integer)
    quantity = Column(Integer)
    status = Column(String, default="pending")  # pending, printing, completed
    order = relationship("PrintOrder", back_populates="items")
