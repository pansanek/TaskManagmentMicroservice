# tests/unit/test_assignee_service.py
import pytest
from uuid import uuid4, UUID
from datetime import datetime, timedelta
from app.services.task_service import TaskService
from app.models.task import TaskStatuses, Task
from app.repositories.task_repo import TaskRepo


@pytest.fixture(scope='session')
def task_service() -> TaskService:
    return TaskService(TaskRepo(clear=True))


@pytest.fixture()
def task_data() -> Task:
    return Task(
        id=UUID('00000000-0000-0000-0000-000000000011'),
        title='Task',
        description='Sample description',
        due_date=datetime.now() + timedelta(days=7),
        status=TaskStatuses.TODO,
        assignee_id=1
    )


def test_empty_tasks(task_service: TaskService) -> None:
    assert task_service.get_tasks() == []


def test_create_task(
        task_data: task_data,
        task_service: TaskService
) -> None:
    task = task_service.create_task(task_data.id, task_data.title, task_data.description, task_data.due_date, task_data.assignee_id)

    assert task.id == task_data.id
    assert task.title == task_data.title
    assert task.description == task_data.description
    assert task.due_date == task_data.due_date
    assert task.status == TaskStatuses.TODO
    assert task.assignee_id == task_data.assignee_id



def test_start_task(
        task_data: task_data,
        task_service: TaskService
) -> None:
    task_service.start_task(task_data.id)
    task = task_service.get_task_by_id(task_data.id)
    assert task.status == TaskStatuses.IN_PROGRESS


def test_complete_task(
        task_data: task_data,
        task_service: TaskService
) -> None:
    task_service.complete_task(task_data.id)
    task = task_service.get_task_by_id(task_data.id)
    assert task.status == TaskStatuses.COMPLETED



def test_get_assignee_task_count(
        task_data: task_data,
        task_service: TaskService
) -> None:
    task_count = task_service.get_assignee_task_count(task_data.assignee_id)
    assert task_count == 1