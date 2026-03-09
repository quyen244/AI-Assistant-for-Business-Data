from fastapi import APIRouter , UploadFile , File , Depends
from src.database.connection import get_db 
from sqlalchemy.orm import Session 
from src.database.schema import DatasetMetadata , DatasetInsights
from src.utils.helper import convert_numpy
from src.llm.insights_generator import generate_insights
import pandas as pd 

router = APIRouter(prefix="/datasets", tags=["datasets"])

@router.get("/")
def get_datasets(db : Session = Depends(get_db)):
    try:
        datasets = db.query(DatasetMetadata).all()
    except Exception as e:
        return {"error": str(e)}
    
    return {"datasets": datasets , 'message' : "succesfully !"}

@router.post("/insights")
def generate_and_get_insights(file : UploadFile = File(...) , db : Session = Depends(get_db)):
    
    df = pd.read_csv(file.file)

    metadata  = {
        "filename": file.filename,
        "columns": df.columns.tolist(),
        "num_rows": len(df),
        "statistics": {
            "numeric": {
                col: {
                    "min": convert_numpy(df[col].min()),
                    "max": convert_numpy(df[col].max()),
                    "mean": convert_numpy(df[col].mean()),
                    "std": convert_numpy(df[col].std())
                }
                for col in df.select_dtypes(include=["number"]).columns
            },
            'categorical' : {
                col : {
                    "unique_values": int(df[col].nunique()),
                    "top_values": df[col].value_counts().head(5).to_dict()
                }
                for col in df.select_dtypes(include=["object"]).columns
            }
        },
        
        "sample_data": df.head(1).to_dict(orient="records")
    }

    dataset_metadata = DatasetMetadata(**metadata)

    res = generate_insights(metadata)

    dataset_insights = DatasetInsights(**res)

    db.add(dataset_metadata)
    db.add(dataset_insights)
    db.commit()
    db.refresh(dataset_metadata)

    return {"message": "Generating insights successfully!", "insights": dataset_insights} 


