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
