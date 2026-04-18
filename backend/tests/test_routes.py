from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from app.main import app

client = TestClient(app)

def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_profile_not_found():
    with patch("app.routes.profile.get_db") as mock_db:
        mock_collection = AsyncMock()
        mock_collection.users.find_one = AsyncMock(return_value=None)
        mock_db.return_value = mock_collection

        response = client.get("/profile/?email=nonexistent@gmail.com")
        assert response.status_code == 404

def test_profile_found():
    with patch("app.routes.profile.get_db") as mock_db:
        mock_collection = AsyncMock()
        mock_collection.users.find_one = AsyncMock(return_value={
            "email": "glitchmybrain@gmail.com",
            "preferences": {
                "tone": "casual",
                "afk_mode": True,
                "timezone": "Asia/Kolkata",
                "rules": []
            },
            "scopes_granted": [],
            "created_at": None,
            "updated_at": None
        })
        mock_db.return_value = mock_collection

        response = client.get("/profile/?email=glitchmybrain@gmail.com")
        assert response.status_code == 200
        assert response.json()["email"] == "glitchmybrain@gmail.com"