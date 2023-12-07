import time
import pytest
import requests
from uuid import UUID, uuid4
from datetime import datetime

from app.models.assignee import Assignee

time.sleep(5)
base_url = 'http://localhost:8000/api/assignees/'

@pytest.fixture(scope='session')
def first_assignee_data() -> dict:
    return {
        'name': 'Assignee 1',
    }

@pytest.fixture(scope='session')
def second_assignee_data() -> dict:
    return {
        'name': 'Assignee 2',
    }

def test_get_assignees_empty() -> None:
    assert requests.get(f'{base_url}/').json() == []

def test_create_assignee_first_success(
        first_assignee_data: dict
) -> None:
    response = requests.post(f'{base_url}/', json=first_assignee_data)
    assignee = response.json()

    assert response.status_code == 200
    assert assignee['name'] == first_assignee_data['name']

def test_create_assignee_first_repeat_error(
        first_assignee_data: dict
) -> None:
    response = requests.post(f'{base_url}/', json=first_assignee_data)

    assert response.status_code == 400

def test_get_assignee_by_id(
        first_assignee_data: dict
) -> None:
    created_assignee = requests.post(f'{base_url}/', json=first_assignee_data).json()
    assignee_id = created_assignee['id']

    retrieved_assignee = requests.get(f'{base_url}/{assignee_id}').json()

    assert retrieved_assignee['name'] == first_assignee_data['name']

def test_update_assignee_name(
        first_assignee_data: dict
) -> None:
    created_assignee = requests.post(f'{base_url}/', json=first_assignee_data).json()
    assignee_id = created_assignee['id']

    updated_assignee_data = {'name': 'Updated Assignee'}
    requests.put(f'{base_url}/{assignee_id}', json=updated_assignee_data)

    retrieved_assignee = requests.get(f'{base_url}/{assignee_id}').json()

    assert retrieved_assignee['name'] == updated_assignee_data['name']

def test_delete_assignee(
        first_assignee_data: dict
) -> None:
    created_assignee = requests.post(f'{base_url}/', json=first_assignee_data).json()
    assignee_id = created_assignee['id']

    requests.delete(f'{base_url}/{assignee_id}')

    assert requests.get(f'{base_url}/{assignee_id}').status_code == 404
