from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    original_activities = deepcopy(activities)

    yield

    activities.clear()
    activities.update(deepcopy(original_activities))


@pytest.fixture
def test_activity_name():
    return "Chess Club"


@pytest.fixture
def new_participant_email():
    return "new.student@mergington.edu"


@pytest.fixture
def existing_participant_email():
    return "michael@mergington.edu"