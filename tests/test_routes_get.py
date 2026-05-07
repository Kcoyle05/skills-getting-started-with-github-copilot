def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_expected_activity_structure(client):
    # Arrange
    expected_activity_count = 9
    expected_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert len(payload) == expected_activity_count
    assert "Chess Club" in payload
    assert expected_fields.issubset(payload["Chess Club"].keys())
    assert isinstance(payload["Chess Club"]["participants"], list)