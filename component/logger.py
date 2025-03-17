"""
Web Application log handler
"""

import os
import logging
from datetime import datetime

# Logging Configuration
log_directory_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
log_format = "[%(asctime)s] [%(levelname)s] [%(filename)s] [%(funcName)s:%(lineno)d] - %(message)s"  # Log4j format

# Create Log Directory
os.makedirs(log_directory_path, exist_ok=True)

# Core Logger function
def get_logger():
        try:
            # Logger filename, file and path configuration
            log_filename = "mtt_document_viewer"
            log_name = f"{datetime.now().strftime('%Y%m%d')}_{log_filename}.log"
            log_path = os.path.join(log_directory_path, log_name)

            # Create Logger
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.DEBUG)

            # Check log handler is existing
            if not logger.hasHandlers():

                # Create Log Formatter
                formatter = logging.Formatter(log_format)

                # Create file handler
                file_handler = logging.FileHandler(log_path, encoding="utf-8")
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)

                # Create console handler
                console_handler = logging.StreamHandler()
                console_handler.setLevel(logging.INFO)
                console_handler.setFormatter(formatter)
                logger.addHandler(console_handler)

            logger.propagate = False # Prevent duplicate logging across different instances
            return logger

        except Exception as err:
            raise RuntimeError(f"An unexpected error occurred while initializing the log function: {err} ")

# Create a global logger instance
logger = get_logger()
