import logging
import sys
from typing import Optional

from django.conf import settings


class Logger:
    """
    Singleton logger instance for the entire project.
    Provides consistent logging configuration and easy access throughout the app.
    """

    _instance: Optional["Logger"] = None
    _logger: Optional[logging.Logger] = None

    def __new__(cls) -> "Logger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup_logger()
        return cls._instance

    def _setup_logger(self):
        """Setup the logger with consistent configuration."""
        self._logger = logging.getLogger("social_media_dashboard")

        # Avoid adding handlers multiple times
        if not self._logger.handlers:
            # Get log level from settings, default to INFO
            log_level = getattr(settings, "LOG_LEVEL", "INFO")
            self._logger.setLevel(getattr(logging, log_level.upper()))

            # Create formatter
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

            # Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self._logger.addHandler(console_handler)

            # File handler if LOG_FILE is specified in settings
            log_file = getattr(settings, "LOG_FILE", None)
            if log_file:
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(formatter)
                self._logger.addHandler(file_handler)

    def debug(self, message: str, *args, **kwargs):
        """Log debug message."""
        self._logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs):
        """Log info message."""
        self._logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        """Log warning message."""
        self._logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        """Log error message."""
        self._logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        """Log critical message."""
        self._logger.critical(message, *args, **kwargs)

    def exception(self, message: str, *args, **kwargs):
        """Log exception with traceback."""
        self._logger.exception(message, *args, **kwargs)


# Convenience function to get logger instance
def get_logger() -> Logger:
    """Get the singleton logger instance."""
    return Logger()


# Module-level logger for easy importing
logger = get_logger()
