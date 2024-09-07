from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import PrintOrderItem, PrintOrder
from sqlalchemy import func

router = APIRouter()

@router.get("/print-batch")
def get_print_batch(db: Session = Depends(get_db)):
    parts_to_print = db.query(
        PrintOrderItem.sample_part_id,
        PrintOrderItem.material_id,
        func.sum(PrintOrderItem.quantity).label('total_quantity')
    ).join(PrintOrderItem.order).filter(PrintOrder.status == 'pending').group_by(
        PrintOrderItem.sample_part_id, PrintOrderItem.material_id
    ).all()

    return [
        {
            "sample_part_id": part.sample_part_id,
            "material_id": part.material_id,
            "total_quantity": part.total_quantity
        } for part in parts_to_print
    ]

