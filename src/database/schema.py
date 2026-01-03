"""
Database schema operations for the test run database.
"""

import logging
from typing import List, Dict, Any, Optional
from .connections import SQLServerConnection
from ..utils.exceptions import SchemaError, DatabaseConnectionError

logger = logging.getLogger(__name__)


class SchemaManager:
    """Manages database schema operations."""
    
    def __init__(self, connection: SQLServerConnection):
        """
        Initialize schema manager.
        
        Args:
            connection: SQL Server connection to the test run database
        """
        self.connection = connection
        self._conn = None
    
    def _ensure_connection(self) -> None:
        """Ensure database connection is established."""
        if not self._conn:
            self._conn = self.connection.connect()
    
    def create_schema(self, schema_file_path: Optional[str] = None) -> bool:
        """
        Create database schema by executing SQL scripts.
        
        Args:
            schema_file_path: Path to schema SQL file. If None, uses default.
            
        Returns:
            True if successful
            
        Raises:
            SchemaError: If schema creation fails
        """
        # TODO: Implement schema creation from SQL files
        logger.info("Schema creation not yet implemented")
        return False
    
    def table_exists(self, table_name: str) -> bool:
        """
        Check if a table exists in the database.
        
        Args:
            table_name: Name of the table to check
            
        Returns:
            True if table exists, False otherwise
        """
        try:
            self._ensure_connection()
            cursor = self._conn.cursor()
            query = """
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = ?
            """
            cursor.execute(query, table_name)
            result = cursor.fetchone()
            return result[0] > 0
        except Exception as e:
            logger.error(f"Error checking table existence: {e}")
            raise SchemaError(f"Failed to check table existence: {e}") from e
    
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Get column information for a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of column information dictionaries
        """
        try:
            self._ensure_connection()
            cursor = self._conn.cursor()
            query = """
                SELECT 
                    COLUMN_NAME,
                    DATA_TYPE,
                    IS_NULLABLE,
                    COLUMN_DEFAULT
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = ?
                ORDER BY ORDINAL_POSITION
            """
            cursor.execute(query, table_name)
            columns = []
            for row in cursor.fetchall():
                columns.append({
                    "name": row[0],
                    "data_type": row[1],
                    "is_nullable": row[2],
                    "default": row[3]
                })
            return columns
        except Exception as e:
            logger.error(f"Error getting table info: {e}")
            raise SchemaError(f"Failed to get table info: {e}") from e

