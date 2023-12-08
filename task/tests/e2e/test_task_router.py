# http://127.0.0.1:8000/api/tasks/

import time
import pytest
import requests
from uuid import UUID, uuid4
from datetime import datetime

from app.models.task import Task,TaskStatuses


time.sleep(5)
base_url = 'http://localhost:80/api/tasks'


@pytest.fixture(scope='session')
def first_task_data() -> Task:
    return Task(
        id = UUID('00000000-0000-0000-0000-000000000011'),
        title='Task 1',
        description = 'Description 1',
        due_date ='2023-12-08T06:36:26.007Z',
        status=TaskStatuses.TODO,
        assignee_id= 1)


@pytest.fixture(scope='session')
def second_task_data() -> Task:
    return Task(
        id = UUID('00000000-0000-0000-0000-000000000012'),
        title='Task 2',
        description = 'Description 2',
        due_date ='2023-12-08T06:36:26.007Z',
        status=TaskStatuses.TODO,
        assignee_id= 2)


def test_get_tasks_empty() -> None:
    assert requests.get(f'{base_url}/').json() == []


def test_create_task_first_success(
        first_task_data: Task
) -> None:
    response = requests.post(f'{base_url}/', json={
        'id': first_task_data.id.hex,
        'title':first_task_data.title,
        'description':first_task_data.description,
        'due_date':str(first_task_data.due_date),
        'status':str(first_task_data.status),
        'assignee_id':first_task_data.assignee_id
    })
    task = response.json()

    assert response.status_code == 200
    assert task['title'] == first_task_data.title
    assert task['status'] == TaskStatuses.TODO.value


def test_create_task_first_repeat_error(
        first_task_data: Task
) -> None:
    response = requests.post(f'{base_url}/',json={
        'id': first_task_data.id.hex,
        'title':first_task_data.title,
        'description':first_task_data.description,
        'due_date':str(first_task_data.due_date),
        'status':str(first_task_data.status),
        'assignee_id':first_task_data.assignee_id
    })

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
        first_task_data: Task
) -> None:
    task_id = first_task_data.id
    result = requests.post(f'{base_url}/{task_id}/start')

    assert result.status_code == 200
    assert result.json()['status'] == TaskStatuses.IN_PROGRESS.value


def test_complete_task_success(
        first_task_data: Task
) -> None:
    task_id = first_task_data.id
    result = requests.post(f'{base_url}/{task_id}/complete')

    assert result.status_code == 200
    assert result.json()['status'] == TaskStatuses.COMPLETED.value




def test_get_tasks_full(
        first_task_data: Task
) -> None:
    tasks = requests.get(f'{base_url}/').json()

    assert len(tasks) == 1
    assert tasks[0]['title'] == first_task_data.title


