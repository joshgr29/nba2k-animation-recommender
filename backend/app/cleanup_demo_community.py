from sqlalchemy import select
from app.database import SessionLocal
from app.models.creator import Creator
from app.models.community_source import CommunitySource
from app.models.animation_review import AnimationReview



def cleanup_demo():
    
    db = SessionLocal()

    creator_cleans = db.scalars(
        select(Creator).where(
            Creator.name.in_([
                "DemoCreator",
                "DemoCreator2",
                "DemoCreator3",
                "DemoCreator4",
                "DemoCreator5"
            ])
        )
    ).all()

    for creator in creator_cleans:
        sources = db.scalars(
            select(CommunitySource).where(
                CommunitySource.creator_id == creator.id
            )
        ).all()

        print(f"{creator.name}: {len(sources)} source(s)")

        for source in sources:
            
            if not source.url.startswith("https://example.com/"):
                unexpected_url = source.url
                db.rollback()
                db.close()
                raise ValueError(f"Unexpected source: {unexpected_url}")
            
            animation_reviews = db.scalars(
                select(AnimationReview).where(
                    AnimationReview.source_id == source.id
                )
            ).all()

            print(f"URL: {source.url}\nNumber of reviews: {len(animation_reviews)}")
            
            
            for review in animation_reviews:
                db.delete(review)

            db.flush()
            db.delete(source)

        db.flush()
        db.delete(creator)

    db.commit()
    db.close()

if __name__ == "__main__":
    cleanup_demo()