import json
from sqlalchemy import select

from app.database import SessionLocal
from app.models import Attribute, AnimationCategory, GameEdition, Season, Animation, RequirementGroup, Requirement

with open("data/nba2k27/dribble_styles.json", "r") as file:
    data = json.load(file)



# print(animation["name"])
# print(animation["category"])
# print(animation["introduced_season"])
# print(animation["requirements"]["logical_operator"])

# for condition in animation["requirements"]["conditions"]:
#     print(condition["attribute"], condition["operator"], condition["value"])
    



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

    if not isinstance(animation["name"], str) or not animation["name"].strip():
        raise ValueError("Animation name must be a non-empty string")

    requirements = animation["requirements"]

    if not isinstance(requirements, dict):
        raise ValueError("Requirements must be a dictionary")

    required_requirement_fields = [
    "logical_operator",
    "conditions",
    ]

    for requirements_field in required_requirement_fields:
        if requirements_field not in requirements:
            raise ValueError(f"Missing field: {requirements_field}")

    if not isinstance(requirements["conditions"], list) or not requirements["conditions"]:
        raise ValueError("Conditions must be a non-empty list")

    if requirements["logical_operator"] not in allowed_logical_operators:
        raise ValueError(
            f"Invalid logical operator: {requirements['logical_operator']}"
    )

    required_conditions_fields = [
        "attribute",
        "operator",
        "value",
    ]

    if animation["category"] not in category_codes:
            raise ValueError(f"Invalid category: {animation['category']}" )
    
    if animation["introduced_season"] not in season_number:
        raise ValueError(f"Invalid season number: {animation['introduced_season']}")

    for condition in requirements["conditions"]:
        if not isinstance(condition, dict):
            raise ValueError("Each condition must be a dictionary")
        for conditions_field in required_conditions_fields:
            if conditions_field not in condition:
                raise ValueError(f"Missing field: {conditions_field}")
        if condition["operator"] not in allowed_operators:
            raise ValueError(f"Invalid operator: {condition['operator']}")
        if condition["attribute"] not in attribute_codes:
            raise ValueError(f"Invalid attribute: {condition['attribute']}")
        if type(condition["value"]) is not int:
            raise ValueError("Requirement value must be an integer")

def import_animation(db, animation, game_edition, attribute_codes, category_codes, season_numbers):

    validate_animation(animation, attribute_codes, category_codes, season_numbers)

    print(f"Animation validated: {animation['name']}")

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

    existing_animation = db.scalar(
        select(Animation).where(
            Animation.name == animation["name"],
            Animation.game_edition_id == game_edition.id,
            Animation.category_id == category.id
        )
    )

    if existing_animation is not None:
        print(f"Animation already exists: {animation['name']}")
    else:
        new_animation = Animation(
            game_edition_id=game_edition.id,
            category_id=category.id,
            introduced_season_id=season.id,
            name=animation["name"]

        )

        db.add(new_animation)
        db.flush()

        new_requirement_group = RequirementGroup(
            animation_id=new_animation.id,
            logical_operator=animation["requirements"]["logical_operator"]
        )

        db.add(new_requirement_group)
        db.flush()

        for condition in animation["requirements"]["conditions"]:
            attribute = db.scalar(
                select(Attribute).where(
                    Attribute.code == condition["attribute"]
                )
            )
            new_requirement = Requirement(
                requirement_group_id=new_requirement_group.id,
                attribute_id=attribute.id,
                operator=condition["operator"],
                value=condition["value"]
            )

            db.add(new_requirement)

        print(f"Animation imported: {animation['name']}")

db = SessionLocal()

try:

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

    for animation in data:
        import_animation(db, animation, game_edition, attribute_codes, category_codes, season_number)
    

    db.commit()

    print("Import completed successfully")

except Exception:
    db.rollback()
    raise

finally:
    db.close()

