import json
from sqlalchemy import select

from app.database import SessionLocal
from app.models import Attribute, AnimationCategory, GameEdition, Season, Animation

with open("data/nba2k27/dribble_styles.json", "r") as file:
    data = json.load(file)



animation = data[0]

# print(animation["name"])
# print(animation["category"])
# print(animation["introduced_season"])
# print(animation["requirements"]["logical_operator"])

# for condition in animation["requirements"]["conditions"]:
#     print(condition["attribute"], condition["operator"], condition["value"])
    

db = SessionLocal()

attribute_codes = db.scalars(
    select(Attribute.code)
).all()

#print(attribute_codes)

category_codes = db.scalars(
    select(AnimationCategory.code)
).all()

#print(category_codes)

game_edition = db.scalar(
    select(GameEdition).where(GameEdition.name == "NBA 2K27")
)

print(game_edition.id)
print(game_edition.name)

season_number = db.scalars(
    select(Season.number).where(
        Season.game_edition_id == game_edition.id
    )
).all()

print(season_number)

category = db.scalar(
    select(AnimationCategory).where(
        AnimationCategory.code == animation["category"]
    )
)

season = db.scalar(
    select(Season).where(
        Season.game_edition_id == game_edition.id,
        Season.number == animation["introduced_season"]
    )
)

new_animation = Animation(
    game_edition_id=game_edition.id,
    category_id=category.id,
    introduced_season_id=season.id,
    name=animation["name"]

)

db.add(new_animation)
db.flush()

print(new_animation.id)
print(new_animation.name)


def validate_animation(animation, attribute_codes, category_codes, season_number):
    required_fields = [
        "name",
        "category",
        "introduced_season",
        "requirements",
    ]

    allowed_operators = [">=", "<=", "="]

    allowed_logical_operators = ["ALL", "ANY"]

    for field in required_fields:
        if field not in animation:
            raise ValueError(f"Missing field: {field}")

    requirements = animation["requirements"]

    required_requirement_fields = [
    "logical_operator",
    "conditions",
    ]

    for requirements_field in required_requirement_fields:
        if requirements_field not in requirements:
            raise ValueError(f"Missing field: {requirements_field}")

    if requirements["logical_operator"] not in allowed_logical_operators:
        raise ValueError(
            f"Invalid logical operator: {requirements['logical_operator']}"
    )

    required_conditions_fields = [
        "attribute",
        "operator",
        "value",
    ]

    for condition in requirements["conditions"]:
        for conditions_field in required_conditions_fields:
            if conditions_field not in condition:
                raise ValueError(f"Missing field: {conditions_field}")
        if condition["operator"] not in allowed_operators:
            raise ValueError(f"Invalid operator: {condition['operator']}")
        if condition["attribute"] not in attribute_codes:
            raise ValueError(f"Invalid attribute: {condition['attribute']}")

    if animation["category"] not in category_codes:
        raise ValueError(f"Invalid category: {animation['category']}" )

    if animation["introduced_season"] not in season_number:
        raise ValueError(f"Invalid season number: {animation['introduced_season']}")

validate_animation(animation, attribute_codes, category_codes, season_number)
print("Animation is valid")

db.close()