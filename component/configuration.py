from utility.filehandler import create_directory

# Upload directory
upload_directory = "/mtt-document-viewer/uploads/"
create_directory(upload_directory)

# Allowed file types
allowed_extension = [".md", ".txt"]

# Max file size (5MB)
max_file_size = 5MB
