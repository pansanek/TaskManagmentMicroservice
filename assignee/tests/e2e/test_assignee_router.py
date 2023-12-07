import pytest
from fastapi.testclient import TestClient
from app.main import app  # Assuming app is your FastAPI application

# Assuming AssigneeService is part of your app
from app.services.assignee_service import AssigneeService

client = TestClient(app)


@pytest.fixture(scope='session')
def assignee_data() -> dict:
    return {
        'name': 'Jon Doe',
    }


def test_create_assignee_success(assignee_data: dict) -> None:
    response = client.post("/api/assignee/", json=assignee_data)
    assert response.status_code == 200
    assert response.json()['name'] == assignee_data['name']


def test_create_assignee_duplicate_error(assignee_data: dict) -> None:
    # Assuming you have a mechanism to prevent duplicate names
    client.post("/api/assignee/", json=assignee_data)

    response = client.post("/api/assignee/", json=assignee_data)
    assert response.status_code == 400


def test_get_assignees_empty() -> None:
    response = client.get("/api/assignee/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_assignees_non_empty(assignee_data: dict) -> None:
    # Create an assignee first
    client.post("/api/assignee/", json=assignee_data)

    response = client.get("/api/assignee/")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_assignee_by_id_success(assignee_data: dict) -> None:
    create_response = client.post("/api/assignee/", json=assignee_data)
    assignee_id = create_response.json()['id']

    response = client.get(f"/api/assignee/{assignee_id}")
    assert response.status_code == 200
    assert response.json()['id'] == assignee_id


def test_get_assignee_by_id_not_found() -> None:
    response = client.get("/api/assignee/123")  # Assuming 123 is a non-existent ID
    assert response.status_code == 404


def test_update_assignee_success(assignee_data: dict) -> None:
    create_response = client.post("/api/assignee/", json=assignee_data)
    assignee_id = create_response.json()['id']

    update_response = client.put(f"/api/assignee/{assignee_id}")

