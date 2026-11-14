from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

    message = response.json()["message"]
    assert message == "NBA 2K Animation Recommender API"

def test_invalide_player_build():
    response = client.post(
        "/recommendations/animations",
        json={
            "height": 78,
            "speed_with_ball": "bonjour",
            "ball_handle": 80
        }
    )
    assert response.status_code == 422