import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


class TestActivitiesAPI:
    """Test suite for the Activities API using AAA pattern"""

    def test_get_activities(self):
        """Test retrieving all activities"""
        # Arrange
        client = TestClient(app)

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data

        # Verify structure of one activity
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)

    def test_signup_for_activity_success(self):
        """Test successful signup for an activity"""
        # Arrange
        client = TestClient(app)
        activity_name = "Chess Club"
        email = "test@example.com"

        # Get initial participants count
        initial_response = client.get("/activities")
        initial_participants = len(initial_response.json()[activity_name]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert f"Signed up {email} for {activity_name}" == data["message"]

        # Verify participant was added
        updated_response = client.get("/activities")
        updated_participants = updated_response.json()[activity_name]["participants"]
        assert len(updated_participants) == initial_participants + 1
        assert email in updated_participants

    def test_signup_for_activity_not_found(self):
        """Test signup for non-existent activity"""
        # Arrange
        client = TestClient(app)
        invalid_activity = "NonExistent Club"
        email = "test@example.com"

        # Act
        response = client.post(
            f"/activities/{invalid_activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" == data["detail"]