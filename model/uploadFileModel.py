"""
Use to validate data before insert into table
"""

from pydantic import BaseModel

class UploadFileModel(BaseModel):
    filename: str
    filepath: str
    filetype: str
    filesize: str
    created_by: str
