# API Documentation

> **Note**: This API documentation is a placeholder and will be expanded as the project develops.

## Overview

This document provides API reference for the SQL Server to Snowflake Query Performance Comparison Tool.

## Configuration API

### ConfigLoader

Main configuration loader class.

**Location**: `src.utils.config_loader`

**Methods**:
- `__init__(config_path: Optional[str] = None)` - Initialize configuration loader
- `get_connection_config(connection_name: str) -> Dict[str, Any]` - Get connection configuration
- `get_execution_config() -> Dict[str, Any]` - Get execution configuration
- `get_ui_config() -> Dict[str, Any]` - Get UI configuration
- `get_logging_config() -> Dict[str, Any]` - Get logging configuration

## Database API

### SQLServerConnection

SQL Server database connection manager.

**Location**: `src.database.connections`

**Methods**:
- `__init__(server: str, database: str, ...)` - Initialize connection parameters
- `connect() -> pyodbc.Connection` - Establish connection
- `disconnect() -> None` - Close connection

### SnowflakeConnection

Snowflake database connection manager.

**Location**: `src.database.connections`

**Methods**:
- `__init__(account: str, warehouse: str, ...)` - Initialize connection parameters
- `connect() -> snowflake.connector.SnowflakeConnection` - Establish connection
- `disconnect() -> None` - Close connection

## Translation API

### QueryTranslator

SQL Server to Snowflake query translator.

**Location**: `src.translation.translator`

**Methods**:
- `translate(sqlserver_query: str) -> str` - Translate SQL Server query to Snowflake
- `validate_translation(snowflake_query: str) -> bool` - Validate translated query

## Execution API

### QueryExecutor

Query execution engine.

**Location**: `src.execution.executor`

**Methods**:
- `execute_sql_server(query: str) -> Dict[str, Any]` - Execute query on SQL Server
- `execute_snowflake(query: str) -> Dict[str, Any]` - Execute query on Snowflake
- `execute_parallel(queries: List[Dict[str, Any]]) -> List[Dict[str, Any]]` - Execute queries in parallel

## Analysis API

### PerformanceComparator

Performance comparison and analysis.

**Location**: `src.analysis.comparator`

**Methods**:
- `compare_results(sqlserver_results: List[Dict], snowflake_results: List[Dict]) -> Dict[str, Any]` - Compare execution results
- `calculate_statistics(results: List[Dict]) -> Dict[str, Any]` - Calculate statistical metrics

## UI API

### MainApplication

Main application window.

**Location**: `src.ui.main`

**Methods**:
- `__init__(config_loader: Optional[ConfigLoader] = None)` - Initialize application
- `run() -> None` - Start application main loop
- `close() -> None` - Close application

## Exception API

### Exception Classes

**Location**: `src.utils.exceptions`

- `SQLServerSnowflakeCompareError` - Base exception class
- `ConfigurationError` - Configuration-related errors
- `DatabaseConnectionError` - Database connection errors
- `QueryExecutionError` - Query execution errors
- `TranslationError` - Translation errors
- `ValidationError` - Validation errors
- `SchemaError` - Schema operation errors

## Logging API

### Logger Functions

**Location**: `src.utils.logger`

- `setup_logger(...)` - Set up logger with configuration
- `get_logger(name: str) -> logging.Logger` - Get logger instance
- `setup_logger_from_config(config_loader) -> logging.Logger` - Set up logger from config
- `get_default_logger() -> logging.Logger` - Get default logger
- `configure_default_logger(config_loader) -> None` - Configure default logger

---

**Note**: This API documentation will be expanded with detailed parameter descriptions, return values, examples, and usage patterns as the project develops.

