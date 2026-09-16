from datetime import date
from sqlalchemy import select

from app.database import SessionLocal
from app.models import (
    Animation,
    AnimationCategory,
    Attribute,
    GameEdition,
    Requirement,
    RequirementGroup,
    Season,
)

def seed_database():
    db = SessionLocal()

    try:
        # Game edition
        game = db.scalar(
            select(GameEdition).where(
                GameEdition.name == "NBA 2K27"
            )
        )

        if game is None:
            game = GameEdition(
                name="NBA 2K27",
                release_date=date(2026, 9, 4),
            )

            db.add(game)
            db.flush()

        # Season
        season = db.scalar(
            select(Season).where(
                Season.game_edition_id == game.id,
                Season.number == 1,
            )
        )

        if season is None:
            season = Season(
                game_edition_id = game.id,
                number=1,
                name="Season 1",
                start_date=date(2026, 9, 4),
                end_date=date(2026, 10, 16),
            )

            db.add(season)
            db.flush()

        #Categories
        categories = [
            ("Jumpshots", "jumpshots"),
            ("Dribble Styles", "dribble_styles"),
            ("Signature Size-Ups", "signature_size_ups"),
            ("Escape Moves", "escape_moves"),
            ("Step Backs", "step_backs"),
            ("Behind the Backs", "behind_the_backs"),
        ]

        for name, code in categories:
            category = db.scalar(
                select(AnimationCategory).where(
                    AnimationCategory.name == name,
                    AnimationCategory.code == code,
                )
            )

            if category is None:
                category = AnimationCategory(
                    name=name,
                    code=code
                )

                db.add(category)
                db.flush()

        #attribute
        attributes = [
            ("Height", "height"),
            ("Three Point", "three_point"),
            ("Mid Range", "mid_range"),
            ("Ball Handle", "ball_handle"),
            ("Speed With Ball", "speed_with_ball"),
        ]

        for name, code in attributes:
            attribute = db.scalar(
                select(Attribute).where(
                    Attribute.name == name,
                    Attribute.code == code,
                )
            )

            if attribute is None:
                attribute = Attribute(
                    name=name,
                    code=code,
                )

                db.add(attribute)
                db.flush()



        db.commit()
        print("Database seeded successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()



if __name__ == "__main__":
    seed_database()

