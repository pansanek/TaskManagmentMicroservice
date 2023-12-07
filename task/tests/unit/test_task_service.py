# tests/unit/test_assignee_service.py
import pytest
from uuid import uuid4, UUID
from datetime import datetime, timedelta
from app.services.task_service import TaskService
from app.models.task import TaskStatuses, Task
from app.repositories.db_task_repo import TaskRepo


@pytest.fixture(scope='session')
def task_service() -> TaskService:
    return TaskService(TaskRepo(clear=True))


@pytest.fixture()
def task_data() -> tuple[UUID, str, str, datetime, int]:
    return (uuid4(), 'Task', 'Task description', datetime.now() + timedelta(days=7), 1)


def test_empty_tasks(task_service: TaskService) -> None:
    assert task_service.get_tasks() == []


def test_create_task(
        task_data: tuple[UUID, str, str, datetime, int],
        task_service: TaskService
) -> None:
    task_id, title, description, due_date, assignee_id = task_data
    task = task_service.create_task(task_id, title, description, due_date, assignee_id)

    assert task.id == task_id
    assert task.title == title
    assert task.description == description
    assert task.due_date == due_date
    assert task.status == TaskStatuses.TODO
    assert task.assignee_id == assignee_id


def test_create_task_duplicate(
        task_data: tuple[UUID, str, str, datetime, int],
        task_service: TaskService
) -> None:
    task_id, title, description, due_date, assignee_id = task_data
    with pytest.raises(KeyError):
        task_service.create_task(task_id, title, description, due_date, assignee_id)


def test_start_task(
        task_data: tuple[UUID, str, str, datetime, int],
        task_service: TaskService
) -> None:
    task_id, _, _, _, _ = task_data
    task_service.start_task(task_id)
    task = task_service.get_task_by_id(task_id)
    assert task.status == TaskStatuses.IN_PROGRESS


def test_complete_task(
        task_data: tuple[UUID, str, str, datetime, int],
        task_service: TaskService
) -> None:
    task_id, _, _, _, _ = task_data
    task_service.start_task(task_id)
    task_service.complete_task(task_id)
    task = task_service.get_task_by_id(task_id)
    assert task.status == TaskStatuses.COMPLETED


def test_cancel_task(
        task_data: tuple[UUID, str, str, datetime, int],
        task_service: TaskService
) -> None:
    task_id, _, _, _, _ = task_data
    task_service.cancel_task(task_id)
    task = task_service.get_task_by_id(task_id)
    assert task.status == TaskStatuses.CANCELED


def test_get_assignee_task_count(
        task_data: tuple[UUID, str, str, datetime, int],
        task_service: TaskService
) -> None:
    _, _, _, _, assignee_id = task_data
    task_count = task_service.get_assignee_task_count(assignee_id)
    assert task_count == 1
