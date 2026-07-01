from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)


def test_unregister_participant_removes_them_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    original_participants = app_module.activities[activity_name]["participants"][:]

    try:
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]

        refreshed_activities = client.get("/activities").json()
        assert email not in refreshed_activities[activity_name]["participants"]
    finally:
        app_module.activities[activity_name]["participants"] = original_participants
