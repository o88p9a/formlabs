from .models import db, Order, OrderItem, Customer

def validate_order(data):
    # Check if customer exists
    customer = Customer.query.get(data['customer_id'])
    if not customer:
        return "Customer not found"

    # Check order item length
    if len(data['items']) > 10:
        return "Order cannot contain more than 10 items"

    # Validate materials
    for item in data['items']:
        if not is_valid_material(item['sample_part_id'], item['material_id']):
            return f"Incompatible sample part {item['sample_part_id']} and material {item['material_id']}"

    return None

def process_order(data):
    order = Order(customer_id=data['customer_id'])
    db.session.add(order)

    for item in data['items']:
        order_item = OrderItem(
            order=order,
            sample_part_id=item['sample_part_id'],
            material_id=item['material_id'],
            quantity=item['quantity']
        )
        db.session.add(order_item)

    db.session.flush()  # Ensure all IDs are generated
    return order

def is_valid_material(sample_part_id, material_id):
    # Assume this function checks the sample part and material compatibility
    compatible_materials = {
        1: [1, 2],  # Sample Part 1 is compatible with Material 1 and 2
        2: [1, 3]   # Sample Part 2 is compatible with Material 1 and 3
    }
    return material_id in compatible_materials.get(sample_part_id, [])
