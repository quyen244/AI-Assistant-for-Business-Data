"""Database query helpers and utilities."""

import time
from typing import List, Dict, Any, Optional

from sqlalchemy import text
from sqlalchemy.orm import Session

from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def execute_query(session: Session, query: str, timeout: int = 30) -> tuple[List[Dict[str, Any]], float]:
    """
    Execute raw SQL query safely.
    
    Args:
        session: SQLAlchemy session
        query: SQL query string
        timeout: Query timeout in seconds
    
    Returns:
        Tuple of (results list, execution time in seconds)
    """
    try:
        start_time = time.time()
        
        # Convert query string to SQLAlchemy text object
        sql_query = text(query)
        
        # Execute query
        result = session.execute(sql_query)
        
        # Fetch results
        rows = result.fetchall()
        
        # Convert to list of dictionaries
        columns = result.keys()
        results = [dict(zip(columns, row)) for row in rows]
        
        execution_time = time.time() - start_time
        
        logger.info(f"Query executed successfully in {execution_time:.2f}s, returned {len(results)} rows")
        
        return results, execution_time
    
    except Exception as e:
        logger.error(f"Query execution failed: {e}")
        raise


def get_table_schema(session: Session, table_name: str) -> List[Dict[str, str]]:
    """
    Get table schema information.
    
    Args:
        session: SQLAlchemy session
        table_name: Name of the table
    
    Returns:
        List of column information dicts
    """
    try:
        inspector_query = f"""
        SELECT name as column_name, type as column_type
        FROM pragma_table_info('{table_name}')
        """
        
        result, _ = execute_query(session, inspector_query)
        logger.info(f"Retrieved schema for table {table_name}")
        return result
    
    except Exception as e:
        logger.error(f"Failed to get table schema: {e}")
        raise


def get_all_tables(session: Session) -> List[str]:
    """
    Get list of all tables in database.
    
    Args:
        session: SQLAlchemy session
    
    Returns:
        List of table names
    """
    try:
        query = """
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        """
        
        results, _ = execute_query(session, query)
        tables = [row['name'] for row in results]
        logger.info(f"Retrieved {len(tables)} tables from database")
        return tables
    
    except Exception as e:
        logger.error(f"Failed to get table list: {e}")
        raise


def get_database_schema_description(session: Session) -> str:
    """
    Get full database schema description for LLM context.
    
    Args:
        session: SQLAlchemy session
    
    Returns:
        Formatted schema description string
    """
    try:
        tables = get_all_tables(session)
        schema_description = ""
        
        for table_name in tables:
            schema_description += f"Table: {table_name}\n"
            schema = get_table_schema(session, table_name)
            for column_info in schema:
                schema_description += f"  - {column_info['column_name']}: {column_info['column_type']}\n"
            schema_description += "\n"
        
        logger.info("Generated database schema description for LLM")
        return schema_description
    
    except Exception as e:
        logger.error(f"Failed to generate schema description: {e}")
        raise


def count_records(session: Session, table_name: str) -> int:
    """
    Count records in a table.
    
    Args:
        session: SQLAlchemy session
        table_name: Name of the table
    
    Returns:
        Number of records
    """
    try:
        query = f"SELECT COUNT(*) as count FROM {table_name}"
        results, _ = execute_query(session, query)
        count = results[0]['count'] if results else 0
        logger.info(f"Table {table_name} has {count} records")
        return count
    
    except Exception as e:
        logger.error(f"Failed to count records: {e}")
        raise


def get_sample_data(session: Session, table_name: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Get sample data from a table.
    
    Args:
        session: SQLAlchemy session
        table_name: Name of the table
        limit: Number of rows to return
    
    Returns:
        List of sample rows
    """
    try:
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        results, _ = execute_query(session, query)
        logger.info(f"Retrieved {len(results)} sample rows from {table_name}")
        return results
    
    except Exception as e:
        logger.error(f"Failed to get sample data: {e}")
        raise
