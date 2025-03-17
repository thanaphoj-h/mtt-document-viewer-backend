from fastapi import FastAPI

app = FastAPI()

# Root Endpoint
@app.get("/")
def root():
    return {"message": "Root Endpoint of MTT Document Viewer API"}
