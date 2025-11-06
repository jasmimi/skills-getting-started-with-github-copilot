from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities_returns_data():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Some known activities should exist
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    test_email = "test_user_clean@example.com"

    # Ensure test email is not already registered
    resp = client.get("/activities")
    assert resp.status_code == 200
    activities = resp.json()
    participants = activities[activity]["participants"]
    if test_email in participants:
        # If it's present (from prior run), remove it first
        del_resp = client.delete(f"/activities/{activity}/unregister?email={test_email}")
        assert del_resp.status_code == 200

    # Sign up
    signup_resp = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert signup_resp.status_code == 200
    assert "Signed up" in signup_resp.json().get("message", "")

    # Verify present
    resp2 = client.get("/activities")
    participants2 = resp2.json()[activity]["participants"]
    assert test_email in participants2

    # Unregister
    del_resp2 = client.delete(f"/activities/{activity}/unregister?email={test_email}")
    assert del_resp2.status_code == 200
    assert "Unregistered" in del_resp2.json().get("message", "")

    # Verify removed
    resp3 = client.get("/activities")
    participants3 = resp3.json()[activity]["participants"]
    assert test_email not in participants3
