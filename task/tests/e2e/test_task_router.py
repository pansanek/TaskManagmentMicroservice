# http://127.0.0.1:8000/api/tasks/

import time
import pytest
import requests
from uuid import UUID, uuid4
from datetime import datetime

from task.app.models.task import Task,TaskStatuses


time.sleep(5)
base_url = 'http://127.0.0.1:8000/api/tasks/'


@pytest.fixture(scope='session')
def first_task_data() -> dict:
    return {
        'title': 'Task',
        'description': 'Description 1',
        'due_date': str(datetime.now()),
        'assignee_id': 1
    }


@pytest.fixture(scope='session')
def second_task_data() -> dict:
    return {
        'title': 'Task 2',
        'description': 'Description 2',
        'due_date': str(datetime.now()),
        'assignee_id': 2
    }


def test_get_tasks_empty() -> None:
    assert requests.get(f'{base_url}/').json() == []


def test_create_task_first_success(
        first_task_data: dict
) -> None:
    response = requests.post(f'{base_url}/', json=first_task_data)
    task = response.json()

    assert response.status_code == 200
    assert task['title'] == first_task_data['title']
    assert task['status'] == TaskStatuses.TODO.value


def test_create_task_first_repeat_error(
        first_task_data: dict
) -> None:
    response = requests.post(f'{base_url}/', json=first_task_data)

    assert response.status_code == 400


def test_start_task_not_found() -> None:
    result = requests.post(f'{base_url}/{uuid4()}/start')
    assert result.status_code == 404


def test_complete_task_not_found() -> None:
    result = requests.post(f'{base_url}/{uuid4()}/complete')
    assert result.status_code == 404


def test_cancel_task_not_found() -> None:
    result = requests.post(f'{base_url}/{uuid4()}/cancel')
    assert result.status_code == 404


def test_start_task_success(
        first_task_data: dict
) -> None:
    response = requests.post(f'{base_url}/', json=first_task_data)
    task_id = response.json()['id']
    result = requests.post(f'{base_url}/{task_id}/start')

    assert result.status_code == 200
    assert result.json()['status'] == TaskStatuses.IN_PROGRESS.value


def test_complete_task_success(
        first_task_data: dict
) -> None:
    response = requests.post(f'{base_url}/', json=first_task_data)
    task_id = response.json()['id']
    result = requests.post(f'{base_url}/{task_id}/complete')

    assert result.status_code == 200
    assert result.json()['status'] == TaskStatuses.COMPLETED.value


def test_cancel_task_success(
        first_task_data: dict
) -> None:
    response = requests.post(f'{base_url}/', json=first_task_data)
    task_id = response.json()['id']
    result = requests.post(f'{base_url}/{task_id}/cancel')

    assert result.status_code == 200
    assert result.json()['status'] == TaskStatuses.CANCELED.value


def test_get_tasks_full(
        first_task_data: dict,
        second_task_data: dict
) -> None:
    tasks = requests.get(f'{base_url}/').json()

    assert len(tasks) == 2
    assert tasks[0]['title'] == first_task_data['title']
    assert tasks[1]['title'] == second_task_data['title']

