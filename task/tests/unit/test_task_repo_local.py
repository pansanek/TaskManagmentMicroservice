import pytest
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from app.models.task import Task, TaskStatuses
from app.repositories.task_repo import TaskRepo

@pytest.fixture(scope='session')
def task_repo() -> TaskRepo:
    return TaskRepo(clear=True)

@pytest.fixture(scope='session')
def sample_task() -> Task:
    return Task(
        id=uuid4(),
        title='Task',
        description='Sample description',
        due_date=datetime.now() + timedelta(days=7),
        status=TaskStatuses.TODO,
        assignee_id=1
    )

def test_empty_list(task_repo: TaskRepo) -> None:
    assert task_repo.get_tasks() == []

def test_create_task(task_repo: TaskRepo, sample_task: Task) -> None:
    created_task = task_repo.create_task(sample_task)
    assert created_task == sample_task

def test_create_task_duplicate(task_repo: TaskRepo, sample_task: Task) -> None:
    with pytest.raises(KeyError):
        task_repo.create_task(sample_task)

def test_get_task_by_id(task_repo: TaskRepo, sample_task: Task) -> None:
    retrieved_task = task_repo.get_task_by_id(sample_task.id)
    assert retrieved_task == sample_task

def test_get_task_by_id_error(task_repo: TaskRepo) -> None:
    with pytest.raises(KeyError):
        task_repo.get_task_by_id(uuid4())

def test_set_status(task_repo: TaskRepo, sample_task: Task) -> None:
    sample_task.status = TaskStatuses.IN_PROGRESS
    updated_task = task_repo.set_status(sample_task)
    assert updated_task.status == TaskStatuses.IN_PROGRESS

    sample_task.status = TaskStatuses.COMPLETED
    updated_task = task_repo.set_status(sample_task)
    assert updated_task.status == TaskStatuses.COMPLETED

    sample_task.status = TaskStatuses.CANCELED
    updated_task = task_repo.set_status(sample_task)
    assert updated_task.status == TaskStatuses.CANCELED

    sample_task.status = TaskStatuses.TODO
    updated_task = task_repo.set_status(sample_task)
    assert updated_task.status == TaskStatuses.TODO
