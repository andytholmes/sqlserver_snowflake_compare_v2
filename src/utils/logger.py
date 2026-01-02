"""
Logging infrastructure for SQL Server to Snowflake Query Performance Comparison Tool.

Provides centralized logging configuration with file and console handlers,
log rotation, and configurable log levels.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional
from datetime import datetime


def setup_logger(
    name: str = "sqlserver_snowflake_compare",
    log_level: str = "INFO",
    log_directory: str = "logs",
    log_filename: str = "sqlserver_snowflake_compare.log",
    file_enabled: bool = True,
    console_enabled: bool = True,
    max_file_size_mb: int = 10,
    backup_count: int = 5,
    format_string: Optional[str] = None,
    date_format: Optional[str] = None
) -> logging.Logger:
    """
    Set up and configure a logger with file and console handlers.
    
    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_directory: Directory for log files
        log_filename: Name of the log file
        file_enabled: Enable file logging
        console_enabled: Enable console logging
        max_file_size_mb: Maximum log file size in MB before rotation
        backup_count: Number of backup log files to keep
        format_string: Custom log format string
        date_format: Custom date format string
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Don't add handlers if they already exist
    if logger.handlers:
        return logger
    
    # Set log level
    level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level)
    
    # Default format strings
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    if date_format is None:
        date_format = "%Y-%m-%d %H:%M:%S"
    
    formatter = logging.Formatter(format_string, datefmt=date_format)
    
    # File handler with rotation
    if file_enabled:
        log_dir = Path(log_directory)
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / log_filename
        max_bytes = max_file_size_mb * 1024 * 1024  # Convert MB to bytes
        
        file_handler = logging.handlers.RotatingFileHandler(
            filename=str(log_file),
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Console handler
    if console_enabled:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger


def get_logger(name: str = "sqlserver_snowflake_compare") -> logging.Logger:
    """
    Get or create a logger instance.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def setup_logger_from_config(config_loader) -> logging.Logger:
    """
    Set up logger using configuration from ConfigLoader.
    
    Args:
        config_loader: ConfigLoader instance with logging configuration
        
    Returns:
        Configured logger instance
    """
    try:
        log_config = config_loader.get_logging_config()
    except AttributeError:
        # Fallback if get_logging_config doesn't exist
        log_config = config_loader.settings.get("logging", {})
    
    return setup_logger(
        name="sqlserver_snowflake_compare",
        log_level=log_config.get("level", "INFO"),
        log_directory=log_config.get("log_directory", "logs"),
        log_filename=log_config.get("log_filename", "sqlserver_snowflake_compare.log"),
        file_enabled=log_config.get("file_enabled", True),
        console_enabled=log_config.get("console_enabled", True),
        max_file_size_mb=log_config.get("max_file_size_mb", 10),
        backup_count=log_config.get("backup_count", 5),
        format_string=log_config.get("format"),
        date_format=log_config.get("date_format")
    )


# Default logger instance (can be reconfigured)
_default_logger: Optional[logging.Logger] = None


def get_default_logger() -> logging.Logger:
    """
    Get the default logger instance, creating it if necessary.
    
    Returns:
        Default logger instance
    """
    global _default_logger
    if _default_logger is None:
        _default_logger = setup_logger()
    return _default_logger


def configure_default_logger(config_loader) -> None:
    """
    Configure the default logger using configuration from ConfigLoader.
    
    Args:
        config_loader: ConfigLoader instance with logging configuration
    """
    global _default_logger
    _default_logger = setup_logger_from_config(config_loader)

