from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), unique=True, nullable=False)

    orders = relationship('Order', back_populates='customer')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    customer = relationship('Customer', back_populates='orders')
    items = relationship('OrderItem', back_populates='order')

    def serialize(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'customer_name': self.customer.name if self.customer else None,
            'items': [item.serialize() for item in self.items]
        }

class OrderItem(Base):
    __tablename__ = 'order_items'

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    order = relationship('Order', back_populates='items')
    sample_part_id = Column(Integer, nullable=False)
    material_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'sample_part_id': self.sample_part_id,
            'material_id': self.material_id,
            'quantity': self.quantity
        }
