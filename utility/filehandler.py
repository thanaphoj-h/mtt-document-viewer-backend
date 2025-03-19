import os
from fastapi import UploadFile
from starlette import datastructures
from typing import Union, List

from component.logger import logger
from utility.commonhandler import validate_unit_and_convert_size


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
    try:
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
    except Exception as err:
        logger.error(f"An unexpected error occurred while validate file extension: {err}")
        raise RuntimeError(f"An unexpected error occurred while validate file extension: {err}")


def validate_file_size(file: Union[str, UploadFile], max_size: str, support_units: list) -> bool:
    """
    Validate the size of file
    :param size: Humanfriendly size of file as [Support GB, MB, KB , B or Bytes (Ex. 1GB, 5MB, 100KB, 10B or 10Bytes)
    """
    try:
        logger.debug(f"Enter validate file size function")
        # Convert Humanfriendly size to integer
        logger.debug(f"Allowed file size: {max_size}")
        max_size = validate_unit_and_convert_size(max_size, support_units)

        # Validate Ordinary File
        if isinstance(file, str):
            logger.debug(f"Detect ordinary file: {file}")
            file_exists = validate_file_exists(file)
            if file_exists:
                file_size = os.path.getsize(file)
                logger.debug(f"Size of {file} is {file_size} Bytes")
                if file_size <= max_size:
                    logger.info(f"File size is not exceed allowed size.")
                    return True
                else:
                    logger.info(f"File size is exceed allowed size.")
                    return False
            else:
                logger.debug(f"File not found: {file}")
                return False
        # Validate FastAPI UploadFile
        elif isinstance(file, datastructures.UploadFile):
            logger.debug(f"Detect FastAPI UploadFile: {file.filename}")
            file.file.seek(0, os.SEEK_END)
            file_size = file.file.tell()
            logger.debug(f"Size of {file.filename} is {file_size} Bytes")
            file.file.seek(0)
            if file_size <= max_size:
                logger.info(f"File size is not exceed allowed size.")
                return True
            else:
                logger.info(f"File size is exceed allowed size.")
                return False
        else:
            logger.error("Unsupported File Type")
            return False
    except Exception as err:
        logger.error(f"An unexpected error occurred while validate file size: {err}")
        raise RuntimeError(f"An unexpected error occurred while validate file size: {err}")
