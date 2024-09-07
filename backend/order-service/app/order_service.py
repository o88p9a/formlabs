from app.models import Order, OrderItem, Customer

def validate_order_data(data):
    if 'customer_id' not in data:
        return "Missing customer_id"

    if 'items' not in data or not isinstance(data['items'], list):
        return "Missing or invalid items"

    for item in data['items']:
        if 'sample_part_id' not in item or 'material_id' not in item or 'quantity' not in item:
            return "Missing item details"
        if not isinstance(item['sample_part_id'], int) or not isinstance(item['material_id'], int) or not isinstance(item['quantity'], int):
            return "Invalid item details"

    return None

def validate_order(data, db):
    customer = db.query(Customer).get(data['customer_id'])
    if not customer:
        return "Customer not found"

    if len(data['items']) > 10:
        return "Order cannot contain more than 10 items"

    for item in data['items']:
        if not is_valid_material(item['sample_part_id'], item['material_id']):
            return f"Incompatible sample part {item['sample_part_id']} and material {item['material_id']}"

    return None

def process_order(data, db):
    order = Order(customer_id=data['customer_id'])
    db.add(order)

    for item in data['items']:
        order_item = OrderItem(
            order=order,
            sample_part_id=item['sample_part_id'],
            material_id=item['material_id'],
            quantity=item['quantity']
        )
        db.add(order_item)

    db.flush()  # Ensure all IDs are generated
    return order

def is_valid_material(sample_part_id, material_id):
    compatible_materials = {
        1: [1, 2],
        2: [1, 3]
    }
    return material_id in compatible_materials.get(sample_part_id, [])
