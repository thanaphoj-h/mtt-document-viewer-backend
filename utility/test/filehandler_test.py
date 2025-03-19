import os
from utility.filehandler import validate_file_exists, validate_file_extension
from component.configuration import allowed_extension
from fastapi import FastAPI, File, UploadFile
from fastapi.testclient import TestClient
from io import BytesIO


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


def test_validate_ordinary_upload_file() -> None:
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
@app.post("/upload/")
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
    response = client.post("/upload/", files={"file": (file_name, file_like, "text/plain")})

    # Print Debug
    print(f"Result test_validate_fastapi_upload_file: {response.json()["valid_extension"]}, "
          f"status code: {response.status_code}")

if __name__ == "__main__":
    test_validate_file_exists()
    test_validate_ordinary_upload_file()
    test_validate_fastapi_upload_file()
