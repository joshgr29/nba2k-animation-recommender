from fastapi import FastAPI, Depends
from pydantic import BaseModel
from app.database import SessionLocal
from app.compatibility import get_compatible_animations
from app.community_scoring import calculate_community_score

class PlayerBuild(BaseModel):
    height: int
    speed_with_ball: int
    ball_handle: int

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "NBA 2K Animation Recommender API"}

@app.post("/recommendations/animations")
def recommend_animations(build: PlayerBuild, db=Depends(get_db)):
    player = {
        "height": build.height,
        "speed_with_ball": build.speed_with_ball,
        "ball_handle": build.ball_handle
    }


    compatible_animations = get_compatible_animations(db, player)

    recommendation = {"compatible_animations": [
                {
                    "name": animation.name,
                    "category": animation.category.code,
                    "community": calculate_community_score(db, animation.id)
                }
                for animation in compatible_animations
            ]
    }

    ranking_reco = sorted(
        recommendation["compatible_animations"],
        key=lambda animation: (
            animation["community"]["recommendation_score"],
            animation["community"]["review_count"] > 0,
            animation["community"]["review_count"]
        ),
        reverse=True
    )

    return {
    "compatible_animations": ranking_reco
}