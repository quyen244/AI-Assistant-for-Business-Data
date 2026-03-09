from sqlalchemy import Column, DateTime, Integer, String, Text , JSON , ForeignKey
from sqlalchemy.orm import declarative_base , relationship
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

    insights = relationship(
        "DatasetInsights",
        back_populates="dataset",
        cascade="all, delete"
    )

class DatasetInsights(Base):
    __tablename__ = 'datasets_insights'

    id = Column(Integer, primary_key = True, index = True)

    dataset_id = Column(Integer, ForeignKey("datasets.id"))

    summary = Column(Text, nullable = False)

    insights = Column(JSON, nullable = False)

    dataset = relationship(
        "DatasetMetadata",
         back_populates="insights"
    )