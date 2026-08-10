import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


@pytest.fixture
def client():
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def restore_activities_state():
    """Restore in-memory activity data after every test for isolation."""
    snapshot = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(snapshot)


def test_get_activities_returns_expected_structure(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload

    chess_club = payload["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_signup_for_activity_success_updates_participants(client):
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    before_count = len(app_module.activities[activity_name]["participants"])

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert len(app_module.activities[activity_name]["participants"]) == before_count + 1
    assert email in app_module.activities[activity_name]["participants"]


def test_signup_for_activity_duplicate_student_returns_400(client):
    activity_name = "Programming Class"
    email = "repeat.student@mergington.edu"

    first_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    second_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_for_unknown_activity_returns_404(client):
    response = client.post("/activities/Unknown%20Activity/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
