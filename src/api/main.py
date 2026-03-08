from fastapi import FastAPI, Path 
from pydantic import BaseModel
import logging 
from src.api.routes import router as dataset_router


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(dataset_router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# uvicorn main:app --reload /py -m uvicorn src.api.main:app --reload