import re
from component.logger import logger

def validate_unit_and_convert_size(size: str, support_unit: list):
    logger.debug(f"Enter validate_unit_and_convert_size function")
    logger.debug(f"Input size: {str(size)}, support_units: {support_unit}")
    try:
        regex_pattern = r"(\d+)([A-Za-z]+)$"
        regex_match = re.findall(regex_pattern, size.strip())
        if regex_match:
            size, unit = regex_match[0]
            size = int(size)
            unit = unit.strip().lower()
            if unit in support_unit:
                if unit == "tb":
                    logger.debug(f"Found unit: {unit}")
                    return tb_to_bytes(size)
                elif unit == "gb":
                    logger.debug(f"Found unit: {unit}")
                    return gb_to_bytes(size)
                elif unit == "mb":
                    logger.debug(f"Found unit: {unit}")
                    return mb_to_bytes(size)
                elif unit == "kb":
                    logger.debug(f"Found unit: {unit}")
                    return kb_to_bytes(size)
                elif unit == "b" or unit == "bytes":
                    logger.debug(f"Found unit: {unit}")
                    return bytes_to_bytes(size)
                else:
                    logger.error(f"Unit is not support: {unit}")
                    return None
            else:
                logger.error(f"Unit is not support: {unit}")
                return None
        else:
            logger.error(f"An unexpected error occurred while matching regex")
            return None
    except Exception as err:
        logger.error(f"An unexpected error occurred while validate unit and convert size: {err}")
        raise RuntimeError(f"An unexpected error occurred while validate unit and convert size: {err}")


def tb_to_bytes(size: int):
    logger.debug(f"Enter tb_to_bytes Function")
    calculate_size = size * 1024 * 1024 * 1024 * 1024
    logger.debug(f"{str(size)} TB is equal to {calculate_size} Bytes")
    return calculate_size


def gb_to_bytes(size: int):
    logger.debug(f"Enter gb_to_bytes Function")
    calculate_size = size * 1024 * 1024 * 1024
    logger.debug(f"{str(size)} GB is equal to {calculate_size} Bytes")
    return calculate_size


def mb_to_bytes(size: int):
    logger.debug(f"Enter mb_to_bytes Function")
    calculate_size = size * 1024 * 1024
    logger.debug(f"{str(size)} MB is equal to {calculate_size} Bytes")
    return calculate_size


def kb_to_bytes(size: int):
    logger.debug(f"Enter kb_to_bytes Function")
    calculate_size = size * 1024
    logger.debug(f"{str(size)} KB is equal to {calculate_size} Bytes")
    return calculate_size


def bytes_to_bytes(size: int):
    logger.debug(f"Enter kb_to_bytes Function")
    calculate_size = size
    logger.debug(f"{str(size)} Bytes is equal to {calculate_size} Bytes")
    return calculate_size
