import time
from app.database import SessionLocal
from app.models import Order, OrderItem, ShippingStatus


def handle_order_printed_event(event):
    db = SessionLocal()

    try:
        order = db.query(Order).filter(Order.id == event["order_id"]).first()
        if order:
            print(f"Order {event['order_id']} already processed.")
            return

        order = Order(
            id=event["order_id"],
            customer_id=event["customer_id"],
            customer_name=event["customer_name"]
        )
        db.add(order)

        for item in event["items"]:
            order_item = OrderItem(
                order_id=order.id,
                sample_part_id=item["sample_part_id"],
                material_id=item["material_id"],
                quantity=item["quantity"]
            )
            db.add(order_item)

        db.commit()

        print(f"Simulating shipping for order {order.id} to {order.customer_name}.")
        time.sleep(5)

        order.status = ShippingStatus.SHIPPED
        db.commit()

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()
