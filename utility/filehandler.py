import os
from component.logger import logger
from fastapi import UploadFile
from starlette import datastructures
from typing import Union, List


def create_directory(directory_path):
    logger.debug(f"Enter create directory function")
    try:
        os.makedirs(directory_path, exist_ok=True)
        logger.info(f"Directory successfully create at: {directory_path}")
    except Exception as err:
        logger.error(f"Failed to create directory: {directory_path}, {err}")
        raise RuntimeError(f"Failed to create directory: {directory_path}, {err}")


def validate_file_exists(file: str) -> bool:
    logger.debug(f"Enter validate file exists function")
    try:
        if os.path.isfile(file):
            logger.debug(f"File is exists: {file}")
            return True
        else:
            logger.debug(f"File is not exists: {file}")
            return False
    except Exception as err:
        logger.error(f"Error occurred while validate file exists: {file}, {err}")
        raise RuntimeError(f"Error occurred while validate file exists: {file}, {err}")


def validate_file_extension(file: Union[str, UploadFile], extensions: Union[str, List[str]]) -> bool:
    """
    Validate the extension of file
    :param: extension (str or tuple) (Ex. ".txt" or (".txt", ".md", ".log")
    """
    logger.debug("Enter Validate file extension function")

    # Convert extension to list (If string is provide)
    if isinstance(extensions, str):
        logger.debug(f"Detected Extension is String: {extensions}")
        # if input extension contained "." remove it
        if "." in extensions:
            extensions = extensions.replace(".", "") # Remove
        allow_extensions = [extensions.lower()]
        logger.debug(f"Convert to Extensions to List with lowercase: {allow_extensions}")
    elif isinstance(extensions, list):
        logger.debug(f"Detected Extension is List: {extensions}")
        allow_extensions = []
        for ext in extensions:
            # if input extension contained "." remove it
            if "." in ext:
                ext = ext.replace(".", "")
            allow_extensions.append(ext.lower())
        logger.debug(f"Convert to lowercase: {allow_extensions}")
    else:
        logger.error("Invalid extension type. Must be either a string or a list of strings.")
        return False

    # Validate ordinary file
    if isinstance(file, str):
        logger.debug(f"Detect Ordinary file: {file}")
        if validate_file_exists(file):
            file_extension = os.path.splitext(file)[1].lower().replace(".", "")
            logger.debug(f"{file} extension is {file_extension}")
            # Check file_extension in allow_extension list
            if file_extension in allow_extensions:
                logger.info(f"{file} extension is valid")
                return True
            else:
                logger.error(f"{file} extension is invalid")
                return False
        else:
            return False

    # Validate FastAPI UploadFile object
    elif isinstance(file, datastructures.UploadFile):
        logger.debug(f"Detect FastAPI UploadFile: {file.filename}")
        file_extension = os.path.splitext(file.filename)[1].lower().replace(".", "")
        logger.debug(f"{file} extension is {file_extension}")
        # Check file_extension in allow_extension list
        if file_extension in allow_extensions:
            logger.info(f"{file} extension is valid")
            return True
        else:
            logger.error(f"{file} extension is invalid")
            return False

    # Error catch if file is not valid
    else:
        logger.error(f"Invalid file type: {type(file)}")
        return False
