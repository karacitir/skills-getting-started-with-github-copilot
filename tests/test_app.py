import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity():
    response = client.post("/activities/Chess Club/signup", params={"email": "test@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Signed up test@example.com for Chess Club" in data["message"]


def test_signup_already_signed_up():
    # First signup
    client.post("/activities/Programming Class/signup", params={"email": "duplicate@example.com"})
    # Try again
    response = client.post("/activities/Programming Class/signup", params={"email": "duplicate@example.com"})
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student already signed up for this activity" in data["detail"]


def test_signup_non_existent_activity():
    response = client.post("/activities/NonExistent/signup", params={"email": "test@example.com"})
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_unregister_from_activity():
    # First signup
    client.post("/activities/Basketball/signup", params={"email": "unregister@example.com"})
    # Then unregister
    response = client.delete("/activities/Basketball/unregister", params={"email": "unregister@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Unregistered unregister@example.com from Basketball" in data["message"]


def test_unregister_not_signed_up():
    response = client.delete("/activities/Gym Class/unregister", params={"email": "notsigned@example.com"})
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student not signed up for this activity" in data["detail"]


def test_unregister_non_existent_activity():
    response = client.delete("/activities/NonExistent/unregister", params={"email": "test@example.com"})
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_root_redirect():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"