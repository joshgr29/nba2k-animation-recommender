from sqlalchemy import select
from app.models.animation_review import AnimationReview
from app.models.community_source import CommunitySource




def calculate_community_score(db, animation_id):
    
    reviews_with_sources = db.execute(
        select(AnimationReview, CommunitySource)
        .join(
            CommunitySource,
            AnimationReview.source_id == CommunitySource.id
        )
        .where(
            AnimationReview.animation_id == animation_id
        )
    ).all()

    score = 0
    positive_count = 0
    negative_count = 0

    latest_reviews = {}

    for review, source in reviews_with_sources:

        creator_id = source.creator_id

        if creator_id not in latest_reviews:
            latest_reviews[creator_id] = (review, source)
        else:
            old_review, old_source = latest_reviews[creator_id]

            if source.published_at > old_source.published_at:
                latest_reviews[creator_id] = (review, source)

    for review, source in latest_reviews.values():
        if review.opinion == "RECOMMENDED":
            score += 1
            positive_count += 1
        elif review.opinion == "CRITICIZED":
            score -= 1
            negative_count += 1
    
    opinion_count = positive_count + negative_count
    recommendation_score = (positive_count - negative_count) / (opinion_count + 5)

    if opinion_count == 0:
        consensus = None
        confidence = None
    else:
        consensus = (abs(positive_count - negative_count)) / opinion_count
        confidence = abs(recommendation_score)
    
    comu_score = {
        "score": score,
        "review_count": len(latest_reviews),
        "creator_count": len(latest_reviews),
        "consensus": consensus,
        "confidence": confidence,
        "recommendation_score": recommendation_score
    }

    return comu_score
