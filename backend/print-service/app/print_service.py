import threading
import time
from queue import Queue
from sqlalchemy import func

from app.app_config import AppConfig
from app.database import SessionLocal
from app.models import PrintOrder, PrintOrderItem

def process_order(order_data):
    db = SessionLocal()
    try:
        print_order = PrintOrder(
            id=order_data['id'],
            customer_id=order_data['customer_id'],
            customer_name=order_data['customer_name'],
            status='pending'
        )
        for item in order_data['items']:
            print_order_item = PrintOrderItem(
                sample_part_id=item['sample_part_id'],
                material_id=item['material_id'],
                quantity=item['quantity'],
                order=print_order
            )
            db.add(print_order_item)

        db.add(print_order)
        db.commit()
    except Exception as e:
        print(f"Error processing order: {e}")
        db.rollback()
    finally:
        db.close()

def simulate_batch_printing(batch, db):
    sample_part_id = batch.sample_part_id
    material_id = batch.material_id
    total_quantity = batch.total_quantity

    print(f"Starting batch print for Sample Part {sample_part_id}, Material {material_id}, Quantity {total_quantity}")

    items_in_batch = db.query(PrintOrderItem).filter(
        PrintOrderItem.sample_part_id == sample_part_id,
        PrintOrderItem.material_id == material_id,
        PrintOrderItem.status == 'pending'
    ).all()

    for item in items_in_batch:
        item.status = 'printing'
        db.commit()
        print(f"Item {item.id} status updated to 'printing' for Sample Part {sample_part_id}, Material {material_id}")

    # simulate printing for each item in the batch
    for item in items_in_batch:
        for i in range(1, item.quantity + 1):
            print(f"Printing unit {i} of {item.quantity} for Sample Part {sample_part_id}...")
            time.sleep(5)

        item.status = 'printed'
        db.commit()
        notify_order_completion_if_ready(db, item.order_id)
        print(f"Item {item.id} for Sample Part {sample_part_id}, Material {material_id} marked as 'printed'.")
   
    print(f"Batch for Sample Part {sample_part_id}, Material {material_id} completed.")

def notify_order_completion_if_ready(db, order_id):
    from app.kafka import get_kafka_producer
    order = db.query(PrintOrder).filter(PrintOrder.id == order_id).one_or_none()

    if order:
        all_items_printed = all(item.status == 'printed' for item in order.items)

        if all_items_printed:
            order.status = 'completed'
            db.commit()
            print(f"Order {order.id} has been marked as completed.")

            kafka_producer = get_kafka_producer()
            kafka_producer.send(AppConfig.ORDER_PRINTED_TOPIC, {
                "order_id": order.id,
                "customer_id": order.customer_id,
                "customer_name": order.customer_name,
                "status": "printed",
                "items": [
                    {
                        "sample_part_id": item.sample_part_id,
                        "material_id": item.material_id,
                        "quantity": item.quantity
                    } for item in order.items
                ]
            })
    print(f"Sent printing complete event for order {order.id}")

def process_batches():
    db = SessionLocal()
    try:
    
        batches = db.query(
            PrintOrderItem.sample_part_id,
            PrintOrderItem.material_id,
            func.sum(PrintOrderItem.quantity).label('total_quantity')
        ).join(PrintOrderItem.order).filter(
            PrintOrder.status == 'pending',
            PrintOrderItem.status == 'pending'
        ).group_by(
            PrintOrderItem.sample_part_id,
            PrintOrderItem.material_id
        ).all()

        queue = Queue()

        stop_event = threading.Event()

        num_worker_threads = 5  
        threads = []
        for _ in range(num_worker_threads):
            thread = threading.Thread(target=worker, args=(queue, stop_event))
            thread.start()
            threads.append(thread)

        # Add batches to the queue
        for batch in batches:
            queue.put(batch)

        # Wait for all batches to be processed
        queue.join()

        # Signal the threads to stop and wait for them to finish
        stop_event.set()
        for _ in range(num_worker_threads):
            queue.put(None)
        for thread in threads:
            thread.join()

        print("All batches processed.")
    finally:
        db.close()

def worker(queue, stop_event):
    while not stop_event.is_set() or not queue.empty():
        batch = queue.get()
        if batch is None:  # Stop signal
            queue.task_done()
            break
        try:
            db = SessionLocal()
            simulate_batch_printing(batch, db)
            db.commit()  # Commit after processing each batch
        except Exception as e:
            print(f"Error processing batch {batch}: {e}")
        finally:
            db.close()
            queue.task_done()

def start_batch_processor():
    while True:
        print("Starting batch processing...")
        process_batches()
        # wait before checking for new batches 
        time.sleep(5)
