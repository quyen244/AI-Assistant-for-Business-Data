from pydantic import BaseModel
from typing import Dict , List

class InsightsResponse(BaseModel):
    message : str
    summary : str 
    insights : List[Dict]