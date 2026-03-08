from pydantic import BaseModel , Field
from typing import Optional, List , Dict
from sqlalchemy import Column, Integer, String, Text , JSON
from sqlalchemy.orm import declarative_base


Base = declarative_base()

class DatasetMetadata(Base):
    __tablename__ = "datasets"
    
    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String(255), nullable=False)

    columns = Column(JSON, nullable=False)

    num_rows = Column(Integer, nullable=False)

    statistics = Column(JSON, nullable=False)

    sample_data = Column(JSON, nullable=False)

    created_at = Column(String(255), nullable=True)