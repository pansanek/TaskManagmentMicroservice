import time
import pytest
import requests
from uuid import UUID, uuid4
from datetime import datetime

from app.models.assignee import Assignee

time.sleep(5)
base_url = 'http://localhost:81/api/assignees'

@pytest.fixture(scope='session')
def first_assignee_data() -> Assignee:
    return Assignee(id=10,name='Name',taskcount=0)

@pytest.fixture(scope='session')
def second_assignee_data() -> Assignee:
    return Assignee(id=12,name='Namee',taskcount=0)

def test_get_assignees_created_in_repo() -> None:
    assert requests.get(f'{base_url}/').json() == []

def test_create_assignee_first_success(
        first_assignee_data: Assignee
) -> None:
    response = requests.post(f'{base_url}/', json={
        'id': first_assignee_data.id,
        'name':first_assignee_data.name,
        'taskcount':first_assignee_data.taskcount
    })
    assignee = response.json()

    assert response.status_code == 200
    assert assignee['name'] == first_assignee_data.name


def test_get_assignee_by_id(
        first_assignee_data: Assignee
) -> None:
    retrieved_assignee = requests.get(f'{base_url}/{first_assignee_data.id}').json()

    assert retrieved_assignee['name'] == first_assignee_data.name

def test_update_assignee(
        first_assignee_data: Assignee
) -> None:
    requests.put(f'{base_url}/{first_assignee_data.id}')

    retrieved_assignee = requests.get(f'{base_url}/{first_assignee_data.id}').json()

    assert retrieved_assignee['taskcount'] == first_assignee_data.taskcount + 1
