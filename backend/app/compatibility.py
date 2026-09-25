from sqlalchemy import select
from app.models import Animation, RequirementGroup, Requirement, Attribute

def check_requirement(player_value, operator, required_value):

    if(operator != ">=" and operator != "<=" and operator != "="):
        raise ValueError(f"Invalid operator: {operator}")
    else:
        if player_value >= required_value and operator == ">=":
            return True
        elif player_value <= required_value and operator == "<=":
            return True
        elif player_value == required_value and operator == "=":
            return True
        return False

def check_requirement_group(player, conditions, logical_operator):

    results = []

    for condition in conditions:

        player_value = player[condition["attribute"]]
        operator = condition["operator"]
        required_value = condition["value"]

        result = check_requirement(player_value, operator, required_value)

        results.append(result)

    if logical_operator == "ALL":
        return all(results)
    elif logical_operator == "ANY":
        return any(results)
    else:
        raise ValueError(f"Invalid logical operator: {logical_operator}")

if __name__ == "__main__":
    player = {
        "height": 78,
        "speed_with_ball": 85
    }

    conditions = [
        {"attribute": "speed_with_ball", "operator": ">=", "value": 79},
        {"attribute": "height", "operator": ">=", "value": 77},
        {"attribute": "height", "operator": "<=", "value": 81}
    ]

    print(check_requirement_group(player, conditions, "ALL"))
    print(check_requirement_group(player, conditions, "ANY"))


def check_animation_compatibility(db, animation, player):
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

        


    animation_compatible = all(group_results) if group_results else False    
    return animation_compatible


def get_compatible_animations(db, player):
    animations = db.scalars(
        select(Animation)
    ).all()

    compatible_animations = []

    for animation in animations:
        if check_animation_compatibility(db, animation, player):
            compatible_animations.append(animation)

    return compatible_animations