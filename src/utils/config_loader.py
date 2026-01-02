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
                Validator("execution.parallel_workers", must_exist=False, gte=1),
                Validator("execution.repeat_count", must_exist=False, gte=1),
                Validator("logging.level", must_exist=False, is_in=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
            ],
        )
        
        if config_file.exists():
            logger.info(f"Loaded configuration from {config_file}")
        else:
            logger.warning("Config file not found. Using defaults from template.")
    
