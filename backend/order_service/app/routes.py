from flask import Blueprint, request, jsonify, current_app
from .models import db, Order, OrderItem, Customer
from .services import validate_order, process_order
from .validators import validate_order_data

bp = Blueprint('routes', __name__)

@bp.route('/order', methods=['POST'])
def place_order():
    data = request.get_json()

    # Validate incoming data
    error = validate_order_data(data)
    if error:
        return jsonify({"error": error}), 400

    # Validate order business rules
    error = validate_order(data)
    if error:
        return jsonify({"error": error}), 400

    # Process the order
    try:
        order = process_order(data)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Failed to process order: {str(e)}")
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

    # Send order to Kafka
    kafka_producer = current_app.config['KAFKA_PRODUCER']
    kafka_producer.send('orders', order.serialize())

    return jsonify({"message": "Order placed successfully!"}), 201

@bp.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([order.serialize() for order in orders]), 200
