"""Database connection and session management."""

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from src.database.schema import Base
from src.utils.config import get_settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

settings = get_settings()

# Create database engine
if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite specific settings
    engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.DATABASE_ECHO,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Enable foreign keys for SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
else:
    # PostgreSQL or other databases
    engine = create_engine(
        settings.DATABASE_URL,
        echo=settings.DATABASE_ECHO,
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        pool_pre_ping=True,  # Verify connections before using them
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    """
    Initialize database by creating all tables.
    Call this function once during application startup.
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


def get_engine():
    """Get database engine instance."""
    return engine


def get_session() -> Session:
    """
    Get database session for dependency injection in FastAPI.
    Usage in FastAPI: Depends(get_session)
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def close_db() -> None:
    """Close database connections."""
    engine.dispose()
    logger.info("Database connections closed")


# Initialize database on module load
if __name__ == "__main__":
    init_db()
