from fastapi import APIRouter , UploadFile , File , Depends , HTTPException
from src.database.connection import get_db 
from sqlalchemy.orm import Session 
from src.database.schema import DatasetMetadata , DatasetInsights
from src.utils.helper import convert_numpy
from src.llm.insights_generator import generate_insights
from src.api.models import InsightsResponse
import pandas as pd 

router = APIRouter(prefix="/datasets", tags=["datasets"])

@router.post("/insights")
def generate_and_get_insights(file : UploadFile = File(...) , db : Session = Depends(get_db)):
    # must be a csv file 
    try:
        df = pd.read_csv(file.file)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CSV file")

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
                for col in df.select_dtypes(include=["object", "category"]).columns
            }
        },
        
        "sample_data": df.head(2).to_dict(orient="records")
    }
    # create and save metadata
    dataset_metadata = DatasetMetadata(**metadata)

    db.add(dataset_metadata)
    db.commit()
    db.refresh(dataset_metadata)
    
    # create and save insights
    res = generate_insights(metadata)

    res['insights'] = res['insights'].model_dump()['insights']

    dataset_insights = DatasetInsights(
        dataset_id=dataset_metadata.id,
        summary=res["summary"],
        insights=res["insights"]
    )

    db.add(dataset_insights)
    db.commit()

    return InsightsResponse(
        message="Generating insights successfully!",
        **res
    )

