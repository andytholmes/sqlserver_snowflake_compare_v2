"""
Database connection management for SQL Server and Snowflake.
"""

import logging
from typing import Optional

import pyodbc
import snowflake.connector

from ..utils.exceptions import DatabaseConnectionError

logger = logging.getLogger(__name__)


class SQLServerConnection:
    """Manages SQL Server database connections."""

    def __init__(
        self,
        server: str,
        database: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        port: int = 1433,
        driver: str = "ODBC Driver 17 for SQL Server",
        **kwargs,
    ):
        """
        Initialize SQL Server connection parameters.

        Args:
            server: SQL Server hostname or instance
            database: Database name
            username: Username for authentication
            password: Password for authentication
            port: Port number (default: 1433)
            driver: ODBC driver name
            **kwargs: Additional connection parameters
        """
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.port = port
        self.driver = driver
        self.connection_params = kwargs
        self.connection: Optional[pyodbc.Connection] = None

    def connect(self) -> pyodbc.Connection:
        """
        Establish connection to SQL Server.

        Returns:
            pyodbc Connection object

        Raises:
            DatabaseConnectionError: If connection fails
        """
        try:
            connection_string = self._build_connection_string()
            self.connection = pyodbc.connect(connection_string)
            logger.info(f"Connected to SQL Server: {self.server}/{self.database}")
            return self.connection
        except Exception as e:
            logger.error(f"Failed to connect to SQL Server: {e}")
            raise DatabaseConnectionError(f"SQL Server connection failed: {e}") from e

    def _build_connection_string(self) -> str:
        """Build ODBC connection string."""
        parts = [
            f"DRIVER={{{self.driver}}}",
            f"SERVER={self.server},{self.port}",
            f"DATABASE={self.database}",
        ]

        if self.username and self.password:
            parts.append(f"UID={self.username}")
            parts.append(f"PWD={self.password}")
        else:
            parts.append("Trusted_Connection=yes")

        return ";".join(parts)

    def disconnect(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("SQL Server connection closed")

    def __enter__(self):
        """Context manager entry."""
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()


class SnowflakeConnection:
    """Manages Snowflake database connections."""

    def __init__(
        self,
        account: str,
        warehouse: str,
        database: str,
        schema: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        role: Optional[str] = None,
        **kwargs,
    ):
        """
        Initialize Snowflake connection parameters.

        Args:
            account: Snowflake account identifier
            warehouse: Warehouse name
            database: Database name
            schema: Schema name
            username: Username for authentication
            password: Password for authentication
            role: Role to use
            **kwargs: Additional connection parameters
        """
        self.account = account
        self.warehouse = warehouse
        self.database = database
        self.schema = schema
        self.username = username
        self.password = password
        self.role = role
        self.connection_params = kwargs
        self.connection: Optional[snowflake.connector.SnowflakeConnection] = None

    def connect(self) -> snowflake.connector.SnowflakeConnection:
        """
        Establish connection to Snowflake.

        Returns:
            Snowflake Connection object

        Raises:
            DatabaseConnectionError: If connection fails
        """
        try:
            conn_params = {
                "account": self.account,
                "warehouse": self.warehouse,
                "database": self.database,
                "schema": self.schema,
                **self.connection_params,
            }

            if self.username and self.password:
                conn_params["user"] = self.username
                conn_params["password"] = self.password

            if self.role:
                conn_params["role"] = self.role

            self.connection = snowflake.connector.connect(**conn_params)
            logger.info(f"Connected to Snowflake: {self.account}/{self.database}/{self.schema}")
            return self.connection
        except Exception as e:
            logger.error(f"Failed to connect to Snowflake: {e}")
            raise DatabaseConnectionError(f"Snowflake connection failed: {e}") from e

    def disconnect(self) -> None:
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("Snowflake connection closed")

    def __enter__(self):
        """Context manager entry."""
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
