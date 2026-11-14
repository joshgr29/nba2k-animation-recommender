from sqlalchemy import select

from app.database import SessionLocal
from app.models import Animation
from app.compatibility import get_compatible_animations

player = {
    "height": 78,
    "speed_with_ball": 85
}

db = SessionLocal()

try:

    compatible_animations = get_compatible_animations(db, player)

    for animation in compatible_animations:
        print(f"{animation.name} compatible")     

    

finally:
    db.close()