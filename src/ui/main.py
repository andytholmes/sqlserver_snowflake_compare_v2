"""
Main UI entry point for SQL Server to Snowflake Query Performance Comparison Tool.
"""

import logging
import tkinter as tk
from tkinter import ttk
from typing import Optional

from ..utils.config_loader import ConfigLoader
from ..utils.logger import setup_logger_from_config

logger = logging.getLogger(__name__)


class MainApplication:
    """Main application window."""

    def __init__(self, config_loader: Optional[ConfigLoader] = None):
        """
        Initialize the main application.

        Args:
            config_loader: Optional ConfigLoader instance
        """
        self.config_loader = config_loader or ConfigLoader()
        self.root = tk.Tk()
        self.root.title("SQL Server to Snowflake Query Performance Comparison")

        # Set window size from config
        ui_config = self.config_loader.settings.get("ui", {})
        width = ui_config.get("window_width", 1200)
        height = ui_config.get("window_height", 800)
        self.root.geometry(f"{width}x{height}")

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the user interface components."""
        # TODO: Implement UI components
        # - Connection configuration panel
        # - Test configuration panel
        # - Translation management panel
        # - Execution progress panel
        # - Results visualization panel

        label = ttk.Label(
            self.root,
            text="SQL Server to Snowflake Query Performance Comparison Tool",
            font=("Arial", 16),
        )
        label.pack(pady=20)

        status_label = ttk.Label(
            self.root, text="UI implementation in progress...", font=("Arial", 12)
        )
        status_label.pack(pady=10)

        logger.info("Main application UI initialized")

    def run(self) -> None:
        """Start the application main loop."""
        logger.info("Starting application")
        self.root.mainloop()

    def close(self) -> None:
        """Close the application."""
        logger.info("Closing application")
        self.root.destroy()


def main():
    """Main entry point for the application."""
    # Load configuration
    config = ConfigLoader()

    # Setup logging
    setup_logger_from_config(config)
    logger.info("Application starting")

    # Create and run application
    app = MainApplication(config_loader=config)
    app.run()


if __name__ == "__main__":
    main()
