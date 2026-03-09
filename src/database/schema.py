from pydantic import BaseModel , Field
from typing import Optional, List , Dict
from sqlalchemy import Column, DateTime, Integer, String, Text , JSON
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class DatasetMetadata(Base):
    __tablename__ = "datasets"
    
    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String(255), nullable=False)

    columns = Column(JSON, nullable=False)

    num_rows = Column(Integer, nullable=False)

    statistics = Column(JSON, nullable=False)

    sample_data = Column(JSON, nullable=False)

    created_at = Column(DateTime, default=datetime.now)

class DatasetInsights(Base):
    __tablename__ = 'datasets_insights'

    id = Column(Integer, primary_key = True, index = True)

    summary = Column(Text, nullable = False)

    insights = Column(JSON, nullable = False)