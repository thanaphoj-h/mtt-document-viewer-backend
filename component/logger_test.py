"""
Web application logger tester
"""

from logger import logger

if __name__ == "__main__":
    logger.debug(f"This is a test of DEBUG log.")
    logger.info(f"This is a test of INFO log.")
    logger.warning(f"This is a test of WARNING log.")
    logger.error(f"This is a test of ERROR log.")
    logger.critical(f"This is a test of CRITICAL log.")
