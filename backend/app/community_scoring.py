from sqlalchemy import select
from app.models.animation_review import AnimationReview



def calculate_community_score(db, animation_id):
    
    reviews = db.scalars(
        select(AnimationReview).where(
            AnimationReview.animation_id == animation_id
        )
    ).all()

    score = 0

    for review in reviews:
        if review.opinion == "RECOMMENDED":
            score += 1
        elif review.opinion == "CRITICIZED":
            score -= 1

    comu_score = {
        "score": score,
        "review_count": len(reviews)
    }

    return comu_score
