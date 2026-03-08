from fastapi import APIRouter , UploadFile , File , Depends
from src.database.connection import get_db 
from sqlalchemy.orm import Session 
from src.database.schema import DatasetMetadata

import pandas as pd 

router = APIRouter(prefix="/datasets", tags=["datasets"])

@router.get("/")
def get_datasets(db : Session = Depends(get_db)):
    try:
        datasets = db.query(DatasetMetadata).all()
    except Exception as e:
        return {"error": str(e)}
    
    return {"datasets": datasets , 'message' : "succesfully !"}

@router.post("/upload")
def upload_csv(file : UploadFile = File(...) , db : Session = Depends(get_db)):

    df = pd.read_csv(file.file)

    metadata  = {
        "filename": file.filename,
        "columns": df.columns.tolist(),
        "num_rows": len(df),
        "statistics": df.describe(include="all").fillna("").to_dict(),
        "sample_data": df.head(5).to_dict(orient="records")
    }

    dataset_metadata = DatasetMetadata(**metadata)
    db.add(dataset_metadata)
    db.commit()
    db.refresh(dataset_metadata)

    return {"message": "Dataset created successfully!", "dataset": metadata} 

@router.get("/{file_id}/insights")
def get_insights(file_id : int, db : Session = Depends(get_db)):
    # Data Profiling 

    return {"message": "Dataset insights retrieved successfully!"}