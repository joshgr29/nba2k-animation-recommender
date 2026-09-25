from fastapi import FastAPI
from pydantic import BaseModel
from app.database import SessionLocal
from app.compatibility import get_compatible_animations

class PlayerBuild(BaseModel):
    height: int
    speed_with_ball: int

app = FastAPI()

@app.get("/")
def root():
    return {"message": "NBA 2K A nimation Recommender API"}

@app.post("/recommendations/animations")
def recommend_animations(build: PlayerBuild):
    player = {
        "height": build.height,
        "speed_with_ball": build.speed_with_ball
    }

    db = SessionLocal()

    try:
        compatible_animations = get_compatible_animations(db, player)

        return {
            "compatible_animations": [
                animation.name
                for animation in compatible_animations
            ]
        }
    finally:
        db.close()