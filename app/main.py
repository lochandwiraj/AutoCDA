from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return {'message': '🚀 AutoCDA API running successfully!'}
