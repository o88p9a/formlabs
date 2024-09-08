from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class ShippingStatus(enum.Enum):
    PENDING = "pending"
    SHIPPED = "shipped"

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)
    customer_name = Column(String, nullable=False)
    status = Column(Enum(ShippingStatus), default=ShippingStatus.PENDING)
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    sample_part_id = Column(Integer, nullable=False)
    material_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    order = relationship("Order", back_populates="items")
