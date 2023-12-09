import pytest
from uuid import  UUID
from datetime import datetime
from app.models.task import Task, TaskStatuses
from app.repositories.db_task_repo import TaskRepo

@pytest.fixture()
def task_repo() -> TaskRepo:
    repo = TaskRepo()
    return repo

@pytest.fixture(scope='session')
def first_task() -> Task:
    return Task(
        id=UUID('998f5a93-8910-46e0-a35f-97cba6222376'),
        title='Task1',
        description='Description for Task 1',
        due_date=datetime.now(),
        status=TaskStatuses.TODO,
        assignee_id=1
    )

@pytest.fixture(scope='session')
def second_task() -> Task:
    return Task(
        id=UUID('8ec239e2-7b8a-4e9f-a05d-e578ab9fc7ea'),
        title='Task 2',
        description='Description for Task 2',
        due_date=datetime.now(),
        status=TaskStatuses.IN_PROGRESS,
        assignee_id=2
    )


def test_create_task(task_repo: TaskRepo, first_task: Task) -> None:
    created_task = task_repo.create_task(first_task)
    assert created_task == first_task

def test_get_task_by_id(task_repo: TaskRepo, first_task: Task) -> None:
    retrieved_task = task_repo.get_task_by_id(first_task.id)
    assert retrieved_task == first_task

def test_set_status(task_repo: TaskRepo, first_task: Task) -> None:
    new_status = TaskStatuses.IN_PROGRESS
    first_task.status = new_status
    updated_task = task_repo.set_status(first_task)
    assert updated_task.status == new_status

def test_start_task(task_repo: TaskRepo, first_task: Task) -> None:
    new_status = TaskStatuses.IN_PROGRESS
    first_task.status = new_status
    started_task = task_repo.start_task(first_task)
    assert started_task.status == new_status
