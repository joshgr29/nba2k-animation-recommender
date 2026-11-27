from app.database import SessionLocal
from app.models.creator import Creator
from app.models.community_source import CommunitySource
from app.models.animation import Animation
from app.models.animation_category import AnimationCategory
from app.models.animation_review import AnimationReview
from app.community_scoring import calculate_community_score
from sqlalchemy import select

from datetime import datetime

import json
from pathlib import Path

file_path = Path(__file__).resolve().parent.parent / "data" / "nba2k27" / "community_reviews.json"


def seed_commu():


    db = SessionLocal()

    with open(file_path, "r", encoding="utf-8") as file:
        real_reviews = json.load(file)

    for review_data in real_reviews:
           

        #creator
        creator = db.scalar(
            select(Creator).where(
                Creator.name == review_data["creator"],
                Creator.platform == review_data["platform"]
            )
        )

        if creator is None:
            
            creator = Creator(name=review_data["creator"], platform=review_data["platform"])
            
            db.add(creator)
            db.commit()
            print("Creator added successfully")
        else:
            print("Creator already exists")

        #community_source
        source = db.scalar(
            select(CommunitySource).where(
                CommunitySource.creator_id == creator.id,
                CommunitySource.url == review_data["url"]
            )
        )

        if source is None:

            source = CommunitySource(creator_id=creator.id, url=review_data["url"], published_at=datetime.fromisoformat(review_data["published_at"]))

            db.add(source)
            db.commit()
            print("Source added successfully")
        else:
            print("Source already exists")

        #review
        animation = db.scalar(
            select(Animation)
            .join(AnimationCategory)
            .where(
                Animation.name == review_data["animation"],
                AnimationCategory.code == review_data["category"]
            )
        )
        if animation is None:
            print(f"Animation not found: {review_data['animation']}")
            continue

        animation_review = db.scalar(
            select(AnimationReview).where(
                AnimationReview.source_id == source.id,
                AnimationReview.animation_id == animation.id
            )
        )

        if animation_review is None:
            animation_review = AnimationReview(source_id=source.id, animation_id=animation.id, opinion=review_data["opinion"])

            db.add(animation_review)
            db.commit()
            print("Animation review added successfully")
        else:
            print("Animation review already exists")


        score = calculate_community_score(db, animation.id)
        print(f"Community score: {score}")
        
    db.close()

if __name__ == "__main__":
    seed_commu()