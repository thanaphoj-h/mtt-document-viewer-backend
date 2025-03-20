import os
from utility.fileHandler import validate_file_exists, validate_file_extension, validate_file_size
from component.configuration import allowed_extension, support_units
from fastapi import FastAPI, File, UploadFile
from fastapi.testclient import TestClient
from io import BytesIO

###############################
# Test a validate_file_exists #
###############################
def test_validate_file_exists():
    # Test validate_file_extension -> Ordinary File
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testfile.txt")
    # Create Mockup File
    with open(file_path, "w") as testfile:
        testfile.write("Hello, this is a test ordinary file")
        testfile.close()

    # Print the test result
    result = validate_file_exists(file_path)
    print(f"Result validate_file_extension: {result}")

    # Delete test file
    os.remove(file_path)

##################################
# Test a validate_file_extension #
##################################
def test_validate_ordinary_upload_file():
    # Test validate_file_extension -> Ordinary File
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testfile.txt")
    # Create Mockup File
    with open (file_path, "w") as testfile:
        testfile.write("Hello, this is a test ordinary file")
        testfile.close()

    # Print the test result
    result = validate_file_extension(file_path, allowed_extension)
    print(f"Result test_validate_ordinary_upload_file: {result}")

    # Delete test file
    os.remove(file_path)


# Create Test API for test UploadFile
app = FastAPI()
@app.post("/test_upload_extension/")
async def upload_file(file: UploadFile = File(...)):
    file_content = await file.read()
    is_valid = validate_file_extension(file, allowed_extension)
    return {"filename": file.filename,
            "valid_extension": is_valid,
            "content_length": len(file_content)}


def test_validate_fastapi_upload_file():
    # Test validate_file_extension -> FastAPI UploadFile
    file_content = b"Hello, this is a test FastAPI UploadFile file"
    file_name = "uploadfile.txt"

    # Simulate an uploadFile instance
    file_like = BytesIO(file_content)
    file_like.name = file_name

    # Simulate an upload request with TestClient
    client = TestClient(app)
    response = client.post("/test_upload_extension/", files={"file": (file_name, file_like, "text/plain")})

    # Print Debug
    print(f"Result test_validate_fastapi_upload_file: {response.json()["valid_extension"]}, "
          f"status code: {response.status_code}")


#############################
# Test a validate_file_size #
#############################
@app.post("/test_upload_size/")
async def upload_file(file: UploadFile = File(...)):
    file_content = await file.read()
    is_valid_size = validate_file_size(file, "5MB", support_units)
    return {"filename": file.filename,
            "valid_size": is_valid_size,
            "content_length": len(file_content)}


def generate_file_with_size(file_path: str, target_size_in_bytes: int, chunk_size: int = 1024):
    """
    Generate a text file with the specified size.
    :param file_path: Path where the file will be saved.
    :param target_size_in_bytes: Target size of the file in bytes.
    Function generated using ChatGPT by OpenAI - ChatGPT Version: GPT-4 (2025-03-20)
    """
    with open(file_path, 'w', encoding="utf-8") as file:
        current_size = 0
        while current_size < target_size_in_bytes:
            remaining_size = target_size_in_bytes - current_size
            # Write a chunk of data; the last chunk might be smaller than the full chunk_size
            if remaining_size < chunk_size:
                content = 'a' * remaining_size  # Write only the remaining size
            else:
                content = 'a' * chunk_size  # Write a full chunk
            file.write(content)  # Write content to file
            # Flush the buffer and ensure it's written to disk
            file.flush()  # Flushes the internal Python buffer to the operating system
            os.fsync(file.fileno())  # Ensures that the data is written to disk immediately
            current_size = os.path.getsize(file_path)  # Get current size of the file
    print(f"File created at {file_path} with size {current_size} bytes.")


def test_validate_ordinary_file_size():

    test_size = [3, 5, 7] # test size in MB
    symbol = ["<", "==", ">"]
    for idx, size in enumerate(test_size):
        print(f"[{idx + 1}] Test File size {symbol[idx]} 5MB")
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "testfile.txt")
        generate_file_with_size(file_path, size * 1024 * 1024)
        result = validate_file_size(file_path, "5MB", support_units)
        print(f"[{idx + 1}] Test Result : {result}")
        os.remove(file_path)

def test_validate_fastapi_upload_size():
    test_size = [3, 5, 7]  # test size in MB
    file_name = "uploadfile.txt"

    for idx, size in enumerate(test_size):
        print(f"Testing file size: {size} MB")

        # Simulate the file content with the required size
        file_content = b'a' * (size * 1024 * 1024)  # Create a byte string of the specified size
        file_like = BytesIO(file_content)
        file_like.name = file_name

        # Simulate an upload request with TestClient
        client = TestClient(app)
        response = client.post("/test_upload_size/", files={"file": (file_name, file_like, "text/plain")})

        # Print Debug
        print(f"Result test_validate_fastapi_upload_file_size ({size} MB): {response.json()['valid_size']}, "
              f"status code: {response.status_code}")


if __name__ == "__main__":
    test_validate_file_exists()
    test_validate_ordinary_upload_file()
    test_validate_fastapi_upload_file()
    test_validate_ordinary_file_size()
    test_validate_fastapi_upload_size()
