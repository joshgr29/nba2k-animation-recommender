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

    demo_reviews = [
        {
            "creator": "DemoCreator2",
            "platform": "YouTube",
            "url": "https://example.com/demo-video-2",
            "animation": "Stephen Curry",
            "category": "dribble_styles",
            "opinion": "RECOMMENDED"
        },
        {
            "creator": "DemoCreator3",
            "platform": "YouTube",
            "url": "https://example.com/demo-video-3",
            "animation": "Kyrie Irving",
            "category": "dribble_styles",
            "opinion": "RECOMMENDED"
        },
        {
            "creator": "DemoCreator4",
            "platform": "TikTok",
            "url": "https://example.com/demo-video-4",
            "animation": "Kyrie Irving",
            "category": "dribble_styles",
            "opinion": "CRITICIZED"
        },
        {
            "creator": "DemoCreator2",
            "platform": "YouTube",
            "url": "https://example.com/demo-video-5",
            "animation": "Stephen Curry",
            "category": "dribble_styles",
            "opinion": "CRITICIZED"
        },
        {
            "creator": "DemoCreator5",
            "platform": "YouTube",
            "url": "https://example.com/demo-video-6",
            "animation": "Kyrie Irving",
            "category": "dribble_styles",
            "opinion": "RECOMMENDED"
        }
    ]

    for review_data in demo_reviews:
           

        #creator
        creator_fictif = db.scalar(
            select(Creator).where(
                Creator.name == review_data["creator"],
                Creator.platform == review_data["platform"]
            )
        )

        if creator_fictif is None:
            
            creator_fictif = Creator(name=review_data["creator"], platform=review_data["platform"])
            
            db.add(creator_fictif)
            db.commit()
            print("Creator added successfully")
        else:
            print("Creator already exists")

        #community_source
        video_fictif = db.scalar(
            select(CommunitySource).where(
                CommunitySource.creator_id == creator_fictif.id,
                CommunitySource.url == review_data["url"]
            )
        )

        if video_fictif is None:

            video_fictif = CommunitySource(creator_id=creator_fictif.id, url=review_data["url"], published_at=datetime.now(timezone.utc))

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
                Animation.name == review_data["animation"],
                AnimationCategory.code == review_data["category"]
            )
        )

        animation_review = db.scalar(
            select(AnimationReview).where(
                AnimationReview.source_id == video_fictif.id,
                AnimationReview.animation_id == animation.id
            )
        )

        if animation_review is None:
            animation_review = AnimationReview(source_id=video_fictif.id, animation_id=animation.id, opinion=review_data["opinion"])

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