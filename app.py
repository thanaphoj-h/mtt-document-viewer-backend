from component.logger import logger
from fastapi import FastAPI
from api.uploadFile import router as upload_file_router

app = FastAPI()

# Include routers
app.include_router(upload_file_router, prefix="/api")

# Root Endpoint
@app.get("/")
def root():
    logger.info(f"Access Root Endpoint")
    return {"message": "Root Endpoint of MTT Document Viewer API"}
