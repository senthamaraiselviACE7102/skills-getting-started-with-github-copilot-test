from src.app import activities


def test_get_activities_returns_activity_catalog(client):
    # Arrange
    endpoint = "/activities"

    # Act
    response = client.get(endpoint)
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert payload

    for activity_name, details in payload.items():
        assert isinstance(activity_name, str)
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details
        assert isinstance(details["participants"], list)


def test_signup_successfully_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"
    assert email not in activities[activity_name]["participants"]

    # Act
    response = client.post(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "new.student@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_signup_duplicate_participant_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    endpoint = f"/activities/{activity_name}/signup"
    assert email in activities[activity_name]["participants"]

    # Act
    response = client.post(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"


def test_unregister_successfully_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    endpoint = f"/activities/{activity_name}/unregister"
    assert email in activities[activity_name]["participants"]

    # Act
    response = client.post(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload == {"message": f"Unregistered {email} from {activity_name}"}
    assert email not in activities[activity_name]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "michael@mergington.edu"
    endpoint = f"/activities/{activity_name}/unregister"

    # Act
    response = client.post(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not.registered@mergington.edu"
    endpoint = f"/activities/{activity_name}/unregister"
    assert email not in activities[activity_name]["participants"]

    # Act
    response = client.post(endpoint, params={"email": email})
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Participant not found for this activity"


def test_root_redirects_to_static_index(client):
    # Arrange
    endpoint = "/"

    # Act
    response = client.get(endpoint, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
