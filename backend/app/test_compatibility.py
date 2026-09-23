from sqlalchemy import select

from app.database import SessionLocal
from app.models import Animation, RequirementGroup, Requirement, Attribute
from app.compatibility import check_requirement_group

player = {
    "height": 75,
    "speed_with_ball": 85
}

db = SessionLocal()

try:
    animations = db.scalars(select(Animation)).all()

    for animation in animations:
        print(f"Animation: {animation.name}")

        groups = db.scalars(
            select(RequirementGroup).where(
                RequirementGroup.animation_id == animation.id
            )
        ).all()

        group_results = []

        for group in groups:

            requirements = db.scalars(
                select(Requirement).where(
                    Requirement.requirement_group_id == group.id
                )
            ).all()

            print(f"Logical operator: {group.logical_operator}")

            conditions = []

            for requirement in requirements:

                attribute = db.scalar(
                    select(Attribute).where(
                        Attribute.id == requirement.attribute_id
                    )
                )

                condition = {
                    "attribute": attribute.code,
                    "operator": requirement.operator,
                    "value": requirement.value
                }

                conditions.append(condition)

            is_compatible = check_requirement_group(
                player,
                conditions,
                group.logical_operator
            )

            group_results.append(is_compatible)

            print(f"Group compatible: {is_compatible}")


        animation_compatible = all(group_results) if group_results else False

        print(f"{animation.name} compatible: {animation_compatible}")     

    

finally:
    db.close()