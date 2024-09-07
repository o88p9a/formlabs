from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Base, Batch

app = FastAPI()

# Database setup
engine = create_engine('sqlite:///sample_parts.db')  # Replace with your database URL
Session = sessionmaker(bind=engine)

@app.get("/batches")
def list_batches():
    session = Session()
    try:
        # Query batches and group by sample part name and material
        results = session.query(
            Batch.sample_part_name,
            Batch.material_id,
            func.sum(Batch.quantity).label('total_quantity')
        ).group_by(Batch.sample_part_name, Batch.material_id).all()

        # Format the results
        batches = [
            {
                'sample_part_name': result.sample_part_name,
                'material': result.material_id,
                'total_quantity': result.total_quantity
            }
            for result in results
        ]

        return batches
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        session.close()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
