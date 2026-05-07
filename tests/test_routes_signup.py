from src.app import activities


def test_signup_adds_new_participant(client, test_activity_name, new_participant_email):
    # Arrange
    participant_count_before = len(activities[test_activity_name]["participants"])

    # Act
    response = client.post(
        f"/activities/{test_activity_name}/signup",
        params={"email": new_participant_email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {new_participant_email} for {test_activity_name}"
    }
    assert len(activities[test_activity_name]["participants"]) == participant_count_before + 1
    assert new_participant_email in activities[test_activity_name]["participants"]


def test_signup_rejects_duplicate_participant(client, test_activity_name, existing_participant_email):
    # Arrange
    expected_error = "Student already signed up for this activity"

    # Act
    response = client.post(
        f"/activities/{test_activity_name}/signup",
        params={"email": existing_participant_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": expected_error}


def test_signup_rejects_unknown_activity(client, new_participant_email):
    # Arrange
    unknown_activity_name = "Robotics Club"

    # Act
    response = client.post(
        f"/activities/{unknown_activity_name}/signup",
        params={"email": new_participant_email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_requires_email_query_parameter(client, test_activity_name):
    # Arrange
    signup_url = f"/activities/{test_activity_name}/signup"

    # Act
    response = client.post(signup_url)

    # Assert
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "email"]