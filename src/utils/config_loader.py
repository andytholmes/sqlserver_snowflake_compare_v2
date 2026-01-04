"""
Configuration loader module for SQL Server to Snowflake Query Performance Comparison Tool.

Uses Dynaconf for robust configuration management with environment variable support.
"""

from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List
import logging
from dynaconf import Dynaconf, Validator

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Loads and manages application configuration using Dynaconf."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration loader.
        
        Args:
            config_path: Path to the configuration JSON file. If None, looks for
                        config.json in the config/ directory.
        """
        self.project_root = Path(__file__).parent.parent.parent
        self.config_dir = self.project_root / "config"
        
        # Determine config file path
        if config_path:
            config_file = Path(config_path)
        else:
            config_file = self.config_dir / "config.json"
            if not config_file.exists():
                config_file = self.config_dir / "config_template.json"
        
        # Initialize Dynaconf with environment variable support
        self.settings = Dynaconf(
            settings_files=[str(config_file)] if config_file.exists() else [],
            envvar_prefix="SQLSERVER_SNOWFLAKE",
            load_dotenv=True,
            dotenv_path=self.project_root / ".env",
            default_settings_path=self.config_dir / "config_template.json",
            environments=False,
            merge_enabled=True,
            validators=[
                # Only validate if the key exists and has a value
                Validator("execution.parallel_workers", condition=lambda v: v is None or v >= 1),
                Validator("execution.repeat_count", condition=lambda v: v is None or v >= 1),
                Validator("logging.level", condition=lambda v: v is None or v in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
            ],
        )
        
        if config_file.exists():
            logger.info(f"Loaded configuration from {config_file}")
        else:
            logger.warning("Config file not found. Using defaults from template.")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation, e.g., "logging.level")
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        return self.settings.get(key, default)
    
    def get_connection_config(self, connection_name: str = "sql_server_test_run") -> Dict[str, Any]:
        """
        Get connection configuration for a specific connection.
        
        Args:
            connection_name: Name of the connection (e.g., "sql_server_test_run", "snowflake")
            
        Returns:
            Dictionary with connection configuration
        """
        return self.settings.get(f"connections.{connection_name}", {})
    
    def get_execution_config(self) -> Dict[str, Any]:
        """
        Get execution configuration.
        
        Returns:
            Dictionary with execution configuration
        """
        return self.settings.get("execution", {})
    
    def get_ui_config(self) -> Dict[str, Any]:
        """
        Get UI configuration.
        
        Returns:
            Dictionary with UI configuration
        """
        return self.settings.get("ui", {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """
        Get logging configuration.
        
        Returns:
            Dictionary with logging configuration
        """
        return self.settings.get("logging", {})
    
    @property
    def config(self) -> Dict[str, Any]:
        """
        Get the full configuration as a dictionary.
        
        Returns:
            Complete configuration dictionary
        """
        return self.settings.as_dict()
    
    def save_config(self, output_path: Optional[str] = None) -> None:
        """
        Save current configuration to a JSON file.
        
        Args:
            output_path: Path to save the configuration. If None, saves to config/config.json
        """
        import json
        
        if output_path is None:
            output_path = self.config_dir / "config.json"
        else:
            output_path = Path(output_path)
        
        with open(output_path, 'w') as f:
            json.dump(self.config, f, indent=2)
        
        logger.info(f"Configuration saved to {output_path}")
    
    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate the current configuration.
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Validate required connections
        connections = self.settings.get("connections", {})
        if not connections:
            errors.append("No connection configurations found")
        
        # Validate logging
        logging_config = self.get_logging_config()
        if not logging_config:
            errors.append("No logging configuration found")
        
        return len(errors) == 0, errors

