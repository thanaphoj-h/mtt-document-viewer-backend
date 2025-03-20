import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from component.database import get_db, create_sql_table
from component.configuration import upload_directory, allowed_extension, max_file_size, support_units, sql_script_directory_path
from utility.fileHandler import validate_file_extension, validate_file_size
from component.logger import logger
from model.uploadFileModel import UploadFileModel

# Initialize router
router = APIRouter()

# Ensure the table exists before handling upload
create_mtt_file_script = os.path.join(sql_script_directory_path, "create_table_mtt_file.sql")
create_sql_table(create_mtt_file_script, "mtt_file")


@router.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):

    # Temporary Variable
    created_by = "system"

    logger.debug("Enter upload file API")
    logger.debug(f"Upload Filename: {file.filename}")

    ###########################
    # Validate File Extension #
    ###########################
    logger.debug("Validate File Extension")
    file_extension = file.filename.split(".")[-1].lower()
    valid_file_extension = validate_file_extension(file, allowed_extension)
    logger.debug(f"Validate File Extension Result: {valid_file_extension}")
    if not valid_file_extension:
        logger.error("Invalid file type (Support .txt and .md)")
        raise HTTPException(status_code=400,
                            detail="Invalid file type (Support .txt and .md)")
    logger.info(f"Validate file extension is passed")

    ######################
    # Validate File Size #
    ######################
    logger.debug("Validate File Size")
    file_size = str(len(await file.read()))
    valid_file_size = validate_file_size(file, max_file_size, support_units)
    logger.debug(f"Validate File Size Result: {valid_file_size}")
    if not valid_file_size:
        logger.error(f"File size is exceeded limit size: {max_file_size}")
        raise HTTPException(status_code=400,
                            detail=f"File size is exceeded limit size: {max_file_size}")
    logger.info(f"Validate file size is passed")

    # Check file exists -> Updated Database (Check Both Database and Directory)
    try:
        logger.debug("Validate File is exists on Database")
        result_check_file_exists_db = db.execute(
            text("CALL mtt_document_viewer.check_file_exists(:filename)"),
            {"filename": file.filename}
        ).fetchone()
        logger.debug(f"Validate file exists on database result: {result_check_file_exists_db[0]}")
        if result_check_file_exists_db and result_check_file_exists_db[0] == "File Exists":
            logger.error(f"File already exists in the database: {file.filename}")
            raise HTTPException(status_code=400,
                                detail=f"File already exists in the database: {file.filename}")
    except SQLAlchemyError as err:
        db.rollback()  # Rollback any changes if an error occurs
        logger.error(f"SQLAlchemy Error occurred: {err}")
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as err:
        db.rollback()  # Rollback any changes if a general error occurs
        logger.error(f"An unexpected error occurred: {err}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {err}")

    # TODO: #########################################################
    # TODO: # Implement a function to update file if file is exists #
    # TODO: #########################################################

    logger.info("Validate file exists on Database is passed")

    #####################
    # Save file to Disk #
    #####################
    try:
        logger.debug("Save file to storage")
        file_path = os.path.join(upload_directory, file.filename)
        logger.debug(f"Save File path: {file_path}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        logger.info(f"File is save to storage at {file_path}")
    except Exception as err:
        logger.error(f"Failed to save file to disk: {str(err)}")
        raise HTTPException(status_code=500,
                            detail=f"Failed to save file to disk: {str(err)}")

    ################################
    # Insert file data to database #
    ################################
    try:
        logger.debug("Insert file data to database")
        logger.debug(f"filename:{file.filename}, filepath:{file_path}, filetype={file_extension}, "
                     f"filesize={file_size}, created_by: {created_by}")
        file_data = UploadFileModel(
            filename=file.filename,
            filepath=file_path,
            filetype=file_extension,
            filesize=file_size,
            created_by=created_by
        )
        logger.debug("Start DB Session and Insert into table")
        logger.debug(f"CALL mtt_document_viewer.insert_upload_file({file.filename}, {file_path}, {file_extension}, "
                     f"{file_size}, {created_by})")
        db.execute(
            text("CALL mtt_document_viewer.insert_upload_file(:filename, :filepath, :filetype, :filesize, :created_by)"),
            {
                "filename": file_data.filename,
                "filepath": file_data.filepath,
                "filetype": file_data.filetype,
                "filesize": file_data.filesize,
                "created_by": file_data.created_by
            }
        )
        db.commit()
        logger.info("File data is successfully insert into database")
    except SQLAlchemyError as err:
        db.rollback()  # Rollback any changes if an error occurs
        logger.error(f"SQLAlchemy Error occurred: {err}")
        raise HTTPException(status_code=500, detail=f"Database error: {err}")
    except Exception as err:
        db.rollback()  # Rollback any changes if a general error occurs
        logger.error(f"An unexpected error occurred: {err}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {err}")

    return {"message": "File uploaded successfully", "filename": file.filename}
