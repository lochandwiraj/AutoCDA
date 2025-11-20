from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "🚀 AutoCDA API running successfully!"}

@app.get("/docs-info")
def docs_info():
    return {"docs": "http://localhost:8000/docs"}
