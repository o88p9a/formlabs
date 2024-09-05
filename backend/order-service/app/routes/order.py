from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

#from ..main import app
from ..models import Order
from ..services.order_service import validate_order, process_order, validate_order_data
from ..database.database import get_db

router = APIRouter()

@router.post("/order", status_code=201)
async def place_order(data: dict, db: Session = Depends(get_db)):
    error = validate_order_data(data)
    if error:
        raise HTTPException(status_code=400, detail=error)

    error = validate_order(data, db)
    if error:
        raise HTTPException(status_code=400, detail=error)

    try:
        order = process_order(data, db)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal server error")

    # Send order to Kafka
    #kafka_producer = app.state.kafka_producer
    #kafka_producer.send('orders', order.serialize())

    return {"message": "Order placed successfully!"}

@router.get("/orders")
async def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return [order.serialize() for order in orders]
