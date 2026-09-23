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