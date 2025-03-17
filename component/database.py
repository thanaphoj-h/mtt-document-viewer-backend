import os
from component.logger import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

# Database Configuration
username = "mtt"
password = "!mtt12345"
host = "192.168.1.150"
port = 3306
database = "mtt_document_viewer"

# Mask password in logs for security
MASKED_DATABASE_URL = f"mysql+pymysql://{username}:******@{host}:{port}/{database}"
logger.info(f"DATABASE_URL: {MASKED_DATABASE_URL}")

# Create Database Engine
DATABASE_URL = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(DATABASE_URL)

# Create Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Get Database Session with Logging
def get_db():
    db = SessionLocal()
    try:
        logger.debug("Database session started.")
        yield db
    except SQLAlchemyError as err:
        logger.error(f"Database Error Occurred: {err}")
        db.rollback()
    finally:
        db.close()
        logger.debug("Database session closed.")


# Function to execute SQL script
def execute_sql_script(script_path):
    """Execute an SQL Script file"""
    logger.debug("Enter Execute SQL Script Function")
    try:
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"SQL Script file not found: {script_path}")

        # Open and read SQL Script file
        with open(script_path, "r", encoding="utf-8") as sql_file:
            sql_commands = sql_file.read()

        # Log the SQL commands for debugging
        logger.debug(f"SQL Commands from {script_path}:\n{sql_commands}")

        # Execute SQL commands
        with engine.connect() as connection:
            connection.execute(text(sql_commands))
            connection.commit()

        logger.info(f"Successfully executed SQL script: {script_path}")

    except FileNotFoundError as err:
        logger.error(str(err))
        raise  # Simply re-raise the original exception

    except Exception as err:
        logger.error(f"Failed to execute SQL script '{script_path}': {err}")
        raise RuntimeError(f"Failed to execute SQL script '{script_path}': {err}")


# Function to create Table
def create_sql_table(script_path, table_name):
    """ Create a table if not exists """
    logger.debug("Enter Create SQL Table Function")
    try:
        with engine.connect() as connection:
            result = connection.execute(text(f"SHOW TABLES LIKE '{table_name}';"))
            table_exists = result.fetchone()  # Returns None if table doesn't exist

        # Log the query result for debugging
        logger.debug(f"Table existence check for '{table_name}': {table_exists}")

        if table_exists:
            logger.info(f"Table '{table_name}' already exists. Skipping SQL execution.")
            return

        # Table does not exist → Run SQL script
        execute_sql_script(script_path)

    except Exception as err:
        logger.error(f"Failed to check or create table '{table_name}': {err}")
        raise RuntimeError(f"Failed to check or create table '{table_name}': {err}")
