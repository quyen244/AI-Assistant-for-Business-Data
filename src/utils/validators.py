"""Input validation utilities."""

import os
from typing import List

from src.utils.config import get_settings
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


def validate_question(question: str, min_length: int = 5) -> bool:
    """
    Validate user question.
    
    Args:
        question: User's natural language question
        min_length: Minimum question length
    
    Returns:
        True if valid, False otherwise
    """
    if not question or len(question.strip()) < min_length:
        logger.warning(f"Invalid question: {question}")
        return False
    return True


def validate_file_format(filename: str) -> bool:
    """
    Validate uploaded file format.
    
    Args:
        filename: Name of the file
    
    Returns:
        True if format is allowed, False otherwise
    """
    settings = get_settings()
    allowed_formats = settings.ALLOWED_FILE_FORMATS.split(",")
    
    file_extension = os.path.splitext(filename)[1].lstrip(".").lower()
    
    if file_extension not in allowed_formats:
        logger.warning(f"Invalid file format: {file_extension}")
        return False
    return True


def validate_file_size(file_size: int) -> bool:
    """
    Validate uploaded file size.
    
    Args:
        file_size: Size of file in bytes
    
    Returns:
        True if size is within limits, False otherwise
    """
    settings = get_settings()
    max_size_bytes = settings.MAX_UPLOAD_FILE_SIZE * 1024 * 1024
    
    if file_size > max_size_bytes:
        logger.warning(f"File size exceeds limit: {file_size} > {max_size_bytes}")
        return False
    return True


def validate_table_name(table_name: str) -> bool:
    """
    Validate table name for SQL safety.
    
    Args:
        table_name: Name of the database table
    
    Returns:
        True if valid, False otherwise
    """
    # Allow alphanumeric and underscores only
    if not all(c.isalnum() or c == "_" for c in table_name):
        logger.warning(f"Invalid table name: {table_name}")
        return False
    
    if not table_name or table_name[0].isdigit():
        logger.warning(f"Invalid table name: {table_name}")
        return False
    
    return True


def validate_sql_query(query: str) -> bool:
    """
    Perform basic SQL query validation for safety.
    
    Args:
        query: SQL query string
    
    Returns:
        True if query appears safe, False otherwise
    """
    # Prevent dangerous operations
    dangerous_keywords = ["DROP", "DELETE", "TRUNCATE", "ALTER", "CREATE"]
    query_upper = query.upper()
    
    for keyword in dangerous_keywords:
        if keyword in query_upper:
            logger.warning(f"Dangerous SQL operation detected: {keyword}")
            return False
    
    return True


def validate_llm_provider(provider: str) -> bool:
    """
    Validate LLM provider selection.
    
    Args:
        provider: Name of LLM provider (gpt or gemini)
    
    Returns:
        True if valid provider, False otherwise
    """
    valid_providers = ["gpt", "gemini"]
    
    if provider.lower() not in valid_providers:
        logger.warning(f"Invalid LLM provider: {provider}")
        return False
    
    return True
