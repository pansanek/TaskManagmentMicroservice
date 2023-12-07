import pytest
from uuid import UUID, uuid4
from fastapi import HTTPException

from app.models.assignee import Assignee
from app.repositories.assignee_repo import AssigneeRepo
from app.services.assignee_service import AssigneeService

@pytest.fixture()
def assignee_repo_with_data():
    repo = AssigneeRepo()
    repo.assignees = [
        Assignee(id=1, name='Павел', taskcount=1),
        Assignee(id=2, name='Макар', taskcount=2),
    ]
    return repo


@pytest.fixture()
def assignee_service_with_repo(assignee_repo_with_data):
    return AssigneeService(assignee_repo=assignee_repo_with_data)


def test_get_assignees(assignee_service_with_repo):
    assignees = assignee_service_with_repo.get_assignees()
    assert len(assignees) == 2
    assert assignees[0].name == 'Павел'
    assert assignees[1].name == 'Макар'


def test_get_assignee_by_id(assignee_service_with_repo):
    assignee = assignee_service_with_repo.get_assignee_by_id(1)
    assert assignee.name == 'Павел'


def test_create_assignee(assignee_service_with_repo):
    new_assignee = assignee_service_with_repo.create_assignee(name='Исполнитель')
    assert new_assignee.name == 'Исполнитель'
    assert new_assignee.taskcount == 0


def test_update_assignee(assignee_service_with_repo):
    updated_assignee = assignee_service_with_repo.update_assignee(id=1)
    assert updated_assignee.taskcount == 2


