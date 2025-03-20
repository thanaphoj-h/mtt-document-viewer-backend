import os
from utility.fileHandler import create_directory

# SQL Script Path
sql_script_directory_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sql")
sql_procedure_directory_path = os.path.join(sql_script_directory_path, "procedure")

# Upload directory
upload_directory = "/mtt-document-viewer/uploads/"
create_directory(upload_directory)

# Allowed file types
allowed_extension = [".md", ".txt"]

# Max file size (5MB)
support_units = ("tb", "gb", "mb", "kb", "b")
max_file_size = "5MB"
