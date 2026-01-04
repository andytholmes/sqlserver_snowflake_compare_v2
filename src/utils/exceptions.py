"""
Base exception classes for SQL Server to Snowflake Query Performance Comparison Tool.
"""


class SQLServerSnowflakeCompareError(Exception):
    """Base exception for all application errors."""

    pass


class ConfigurationError(SQLServerSnowflakeCompareError):
    """Raised when there's a configuration error."""

    pass


class DatabaseConnectionError(SQLServerSnowflakeCompareError):
    """Raised when database connection fails."""

    pass


class QueryExecutionError(SQLServerSnowflakeCompareError):
    """Raised when query execution fails."""

    pass


class TranslationError(SQLServerSnowflakeCompareError):
    """Raised when query translation fails."""

    pass


class ValidationError(SQLServerSnowflakeCompareError):
    """Raised when validation fails."""

    pass


class SchemaError(SQLServerSnowflakeCompareError):
    """Raised when database schema operations fail."""

    pass
