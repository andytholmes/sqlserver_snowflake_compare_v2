#!/usr/bin/env python3
"""
Main entry point for SQL Server to Snowflake Query Performance Comparison Tool.

This is the command-line entry point for the application.
"""

import sys
import argparse
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src import __version__
from src.utils.config_loader import ConfigLoader
from src.utils.logger import setup_logger_from_config
from src.ui.main import MainApplication


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="SQL Server to Snowflake Query Performance Comparison Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Start GUI application
  %(prog)s --config custom.json  # Use custom config file
  %(prog)s --version           # Show version information
        """
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to configuration file (default: config/config.json)"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default=None,
        help="Override log level from configuration"
    )
    
    parser.add_argument(
        "--no-gui",
        action="store_true",
        help="Run in CLI mode (GUI not implemented yet)"
    )
    
    return parser.parse_args()


def initialize_application(config_path=None, log_level=None):
    """
    Initialize the application with configuration and logging.
    
    Args:
        config_path: Optional path to configuration file
        log_level: Optional log level override
        
    Returns:
        ConfigLoader instance
    """
    # Load configuration
    config = ConfigLoader(config_path=config_path)
    
    # Override log level if specified
    if log_level:
        config.settings.set("logging.level", log_level)
    
    # Setup logging
    setup_logger_from_config(config)
    logger = logging.getLogger(__name__)
    
    # Log startup information
    logger.info("=" * 60)
    logger.info(f"SQL Server to Snowflake Query Performance Comparison Tool")
    logger.info(f"Version: {__version__}")
    logger.info(f"Python: {sys.version.split()[0]}")
    logger.info("=" * 60)
    
    return config


def main():
    """Main entry point for the application."""
    try:
        # Parse command-line arguments
        args = parse_arguments()
        
        # Initialize application
        config = initialize_application(
            config_path=args.config,
            log_level=args.log_level
        )
        
        logger = logging.getLogger(__name__)
        
        if args.no_gui:
            logger.info("CLI mode requested (not yet implemented)")
            logger.info("Starting GUI mode instead...")
        
        # Create and run GUI application
        logger.info("Initializing GUI application...")
        app = MainApplication(config_loader=config)
        app.run()
        
        logger.info("Application exited normally")
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        logging.exception("Unhandled exception in main")
        sys.exit(1)


if __name__ == "__main__":
    main()

