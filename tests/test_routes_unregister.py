from src.app import activities


def test_unregister_removes_existing_participant(client, test_activity_name, existing_participant_email):
    # Arrange
    participant_count_before = len(activities[test_activity_name]["participants"])

    # Act
    response = client.delete(
        f"/activities/{test_activity_name}/signup",
        params={"email": existing_participant_email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {existing_participant_email} from {test_activity_name}"
    }
    assert len(activities[test_activity_name]["participants"]) == participant_count_before - 1
    assert existing_participant_email not in activities[test_activity_name]["participants"]


def test_unregister_rejects_non_member(client, test_activity_name, new_participant_email):
    # Arrange
    expected_error = "Student is not signed up for this activity"

    # Act
    response = client.delete(
        f"/activities/{test_activity_name}/signup",
        params={"email": new_participant_email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": expected_error}


def test_unregister_rejects_unknown_activity(client, existing_participant_email):
    # Arrange
    unknown_activity_name = "Robotics Club"

    # Act
    response = client.delete(
        f"/activities/{unknown_activity_name}/signup",
        params={"email": existing_participant_email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_requires_email_query_parameter(client, test_activity_name):
    # Arrange
    unregister_url = f"/activities/{test_activity_name}/signup"

    # Act
    response = client.delete(unregister_url)

    # Assert
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "email"]