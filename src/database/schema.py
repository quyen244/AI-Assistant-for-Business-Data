"""SQLAlchemy database models/schema."""

from datetime import datetime
from decimal import Decimal

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Product(Base):
    """Product table model."""
    
    __tablename__ = "products"
    
    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(255), index=True, nullable=False)
    category = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    sales = relationship("Sale", back_populates="product", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Product(product_id={self.product_id}, name={self.product_name})>"


class Sale(Base):
    """Sales table model."""
    
    __tablename__ = "sales"
    
    sale_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    sale_date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    revenue = Column(Float, nullable=False)
    
    # Relationships
    product = relationship("Product", back_populates="sales")
    
    def __repr__(self) -> str:
        return f"<Sale(sale_id={self.sale_id}, product_id={self.product_id}, revenue={self.revenue})>"


class Customer(Base):
    """Customers table model."""
    
    __tablename__ = "customers"
    
    customer_id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    country = Column(String(100), nullable=False)
    registration_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self) -> str:
        return f"<Customer(customer_id={self.customer_id}, name={self.customer_name})>"


class QueryHistory(Base):
    """Query history for tracking user queries."""
    
    __tablename__ = "query_history"
    
    query_id = Column(Integer, primary_key=True, index=True)
    user_question = Column(String(512), nullable=False)
    generated_sql = Column(String(2000), nullable=False)
    results_count = Column(Integer, default=0)
    execution_time = Column(Float, default=0.0)
    llm_provider = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self) -> str:
        return f"<QueryHistory(query_id={self.query_id}, provider={self.llm_provider})>"
