import requests
from bs4 import BeautifulSoup
import json

url_dribble_styles = "https://www.lockercodes.io/nba-2k/animation-requirements/all-dribble-moves/dribble-style"
url_signature_size_ups = "https://www.lockercodes.io/nba-2k/animation-requirements/all-dribble-moves/signature-size-up"
url_escape_moves = "https://www.lockercodes.io/nba-2k/animation-requirements/all-dribble-moves/escape-moves"

def height_to_inches(height):
    feet, inches = height.split("'")

    inches = inches.replace('"', '')

    feet = int(feet)
    inches = int(inches)
    return feet * 12 + inches





def generate_category(url, category, attribute):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    
    print(response.status_code)

    table = soup.find("table")

    rows = table.find_all("tr")
    print(len(rows))

    animations = []

    for row in rows[1:]:
        cells = row.find_all("td")

        name = cells[0].get_text(" ", strip=True)
        attribute_value = int(cells[1].get_text(strip=True))
        min_height = height_to_inches(cells[2].get_text(strip=True))
        max_height = height_to_inches(cells[3].get_text(strip=True))

        animation = {
            "name": name,
            "category": category,
            "introduced_season": 1,
            "requirements": {
                "logical_operator": "ALL",
                "conditions":[
                    {
                        "attribute": attribute,
                    "operator": ">=",
                    "value": attribute_value
                },
                {
                    "attribute": "height",
                    "operator": ">=",
                    "value": min_height
                },
                {
                    "attribute": "height",
                    "operator": "<=",
                    "value": max_height
                    }
                ]
            }
        }

        animations.append(animation)
  

    with open(f"data/nba2k27/{category}.json", "w") as file:
        json.dump(animations, file, indent=4)

    print(f"{len(animations)} animations generated")

generate_category(url_dribble_styles, "dribble_styles", "speed_with_ball")
generate_category(url_signature_size_ups, "signature_size_ups", "ball_handle")
generate_category(url_escape_moves, "escape_moves", "ball_handle")