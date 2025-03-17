from component.logger import logger
from fastapi import FastAPI

app = FastAPI()

# Root Endpoint
@app.get("/")
def root():
    logger.info(f"Access Root Endpoint")
    return {"message": "Root Endpoint of MTT Document Viewer API"}
