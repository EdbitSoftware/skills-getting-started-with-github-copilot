import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)

def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Ensure user is not already signed up
    client.delete(f"/activities/{activity}/participants/{email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert f"Signed up {email} for {activity}" in response.json()["message"]
    # Double signup should fail
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    # Remove participant
    response3 = client.delete(f"/activities/{activity}/participants/{email}")
    assert response3.status_code == 200
    assert f"Removed {email} from {activity}" in response3.json()["message"]

def test_remove_nonexistent_participant():
    response = client.delete("/activities/Chess%20Club/participants/nonexistent@mergington.edu")
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]

def test_signup_nonexistent_activity():
    response = client.post("/activities/NonexistentActivity/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
