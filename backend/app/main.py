from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "NBA 2K A nimation Recommender API"}