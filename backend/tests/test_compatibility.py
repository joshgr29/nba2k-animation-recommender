from app.compatibility import check_requirement, check_requirement_group
import pytest

def test_greater_or_equal():
    assert check_requirement(75, ">=", 60)

def test_less_or_equal_false():
    assert check_requirement(75, "<=", 60) is False

def test_invalid_operator():
    with pytest.raises(ValueError):
        check_requirement(75, ">", 60)

def test_requirement_group_all():
    player = {
        "height": 78,
        "speed_with_ball": 85,
        "ball_handle": 90,
        "three_point": 82
    }

    conditions = [{"attribute":"height", "operator":">=", "value":75},
                 {"attribute":"height", "operator":"<=", "value":80},
                 {"attribute":"speed_with_ball", "operator": ">=", "value": 80}]
    assert check_requirement_group(player, conditions, "ALL") is True

def test_requirement_group_all_false():
        player = {
            "height": 70,
            "speed_with_ball": 85,
            "ball_handle": 90,
            "three_point": 82
        }
    
        conditions = [{"attribute":"height", "operator":">=", "value":75},
                     {"attribute":"height", "operator":"<=", "value":80},
                     {"attribute":"speed_with_ball", "operator": ">=", "value": 80}]
        assert check_requirement_group(player, conditions, "ALL") is False


def test_requirement_group_any():
    player = {
        "three_point": 78,
        "mid_range": 90
    }

    conditions = [{"attribute":"three_point", "operator": ">=", "value": 80},
                  {"attribute":"mid_range", "operator": ">=", "value": 85}]
    assert check_requirement_group(player, conditions, "ANY") is True

def test_requirement_group_any_false():
    player = {
        "three_point": 78,
        "mid_range": 82
    }

    conditions = [{"attribute":"three_point", "operator": ">=", "value": 80},
                    {"attribute":"mid_range", "operator": ">=", "value": 85}]
    assert check_requirement_group(player, conditions, "ANY") is False