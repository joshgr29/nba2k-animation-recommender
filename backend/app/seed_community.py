from app.database import SessionLocal
from app.models.creator import Creator
from app.models.community_source import CommunitySource
from app.models.animation import Animation
from app.models.animation_category import AnimationCategory
from app.models.animation_review import AnimationReview
from app.community_scoring import calculate_community_score
from sqlalchemy import select

from datetime import datetime, timezone


def seed_commu():
    
    db = SessionLocal()

    #creator
    creator_fictif = db.scalar(
        select(Creator).where(
            Creator.name == "DemoCreator",
            Creator.platform == "YouTube"
        )
    )

    if creator_fictif is None:
        
        creator_fictif = Creator(name="DemoCreator", platform="YouTube")
        
        db.add(creator_fictif)
        db.commit()
        print("Creator added successfully")
    else:
        print("Creator already exists")

    #community_score
    video_fictif = db.scalar(
        select(CommunitySource).where(
            CommunitySource.creator_id == creator_fictif.id,
            CommunitySource.url == "https://example.com/demo-video"
        )
    )

    if video_fictif is None:

        video_fictif = CommunitySource(creator_id=creator_fictif.id, url="https://example.com/demo-video", published_at=datetime.now(timezone.utc))

        db.add(video_fictif)
        db.commit()
        print("Video added successfully")
    else:
        print("Video already exists")

    #review
    animation = db.scalar(
        select(Animation)
        .join(AnimationCategory)
        .where(
            Animation.name == "Stephen Curry",
            AnimationCategory.code == "dribble_styles"
        )
    )

    animation_review = db.scalar(
        select(AnimationReview).where(
            AnimationReview.source_id == video_fictif.id,
            AnimationReview.animation_id == animation.id
        )
    )

    if animation_review is None:
        animation_review = AnimationReview(source_id=video_fictif.id, animation_id=animation.id, opinion="RECOMMENDED")

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