from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import PrintOrderItem, PrintOrder
from app.models import Status

router = APIRouter()

@router.get("/print-batch", status_code=status.HTTP_200_OK)
async def get_print_batch(db: Session = Depends(get_db)):
    try:
        parts_to_print = db.query(
            PrintOrderItem.sample_part_id,
            PrintOrderItem.material_id,
            func.sum(PrintOrderItem.quantity).label('total_quantity')
        ).join(PrintOrderItem.order).filter(PrintOrder.status == Status.PENDING).group_by(
            PrintOrderItem.sample_part_id, PrintOrderItem.material_id
        ).all()

        result = [
            {
                "sample_part_id": part.sample_part_id,
                "material_id": part.material_id,
                "total_quantity": part.total_quantity
            } for part in parts_to_print
        ]

        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error occurred while fetching the print batch."
        )
