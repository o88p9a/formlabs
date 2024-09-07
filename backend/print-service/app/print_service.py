import time
from app.database import SessionLocal
from kafka import KafkaProducer
from app.kafka import get_kafka_producer
from app.models import PrintOrder


def simulate_printing(print_order):
    for item in print_order.items:
        print(f"Printing sample part {item.sample_part_id} with material {item.material_id}, quantity {item.quantity}")
        time.sleep(2)  # Simulate print time for each item

    print(f"All parts for order {print_order.id} printed.")
    return True

def notify_printing_complete(kafka_producer: KafkaProducer, print_order):
    message = {
        "order_id": print_order.id,
        "customer_id": print_order.customer_id,
        "customer_name": print_order.customer_name,
        "status": "printed",
        "items": [
            {
                "sample_part_id": item.sample_part_id,
                "material_id": item.material_id,
                "quantity": item.quantity
            } for item in print_order.items
        ]
    }

    kafka_producer.send("order_printed", message)
    print(f"Sent printing complete event for order {print_order.id}")

# Process a print order
def process_print_order(order_id: int):
    db = SessionLocal()
    print_order = db.query(PrintOrder).get(order_id)

    if print_order and print_order.status == 'pending':
        if simulate_printing(print_order):
            print_order.status = 'completed'
            db.commit()
            kafka_producer = get_kafka_producer() 
            notify_printing_complete(kafka_producer, print_order)

    db.close()
