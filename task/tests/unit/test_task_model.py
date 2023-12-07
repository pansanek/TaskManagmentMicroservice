# /tests/unit/test_assignee_model.py

import pytest
from uuid import uuid4
from datetime import datetime
from pydantic import ValidationError

from app.models.task import Task, TaskStatuses


@pytest.fixture()
def any_task_data() -> dict:
    return {
        'id': uuid4(),
        'title': 'Title',
        'description': 'Task Description',
        'due_date': datetime.now(),
        'status': TaskStatuses.TODO,
        'assignee_id': 1
    }


def test_task_creation(any_task_data: dict):
    task = Task(**any_task_data)

    assert dict(task) == any_task_data


def test_task_missing_title(any_task_data: dict):
    any_task_data.pop('title')

    with pytest.raises(ValidationError):
        Task(**any_task_data)


def test_task_missing_due_date(any_task_data: dict):
    any_task_data.pop('due_date')

    with pytest.raises(ValidationError):
        Task(**any_task_data)


def test_task_invalid_status(any_task_data: dict):
    any_task_data['status'] = 'invalid_status'

    with pytest.raises(ValidationError):
        Task(**any_task_data)
