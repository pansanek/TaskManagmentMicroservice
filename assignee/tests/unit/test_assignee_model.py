import pytest
from uuid import UUID, uuid4
from fastapi import HTTPException

from assignee import Assignee
from assignee_repo import AssigneeRepo
from assignee_service import AssigneeService


@pytest.fixture()
def assignee_repo_with_data():
    repo = AssigneeRepo()
    repo.assignees = [
        Assignee(id=UUID('00000000-0000-0000-0000-000000000001'), name='Павел', taskcount=1),
        Assignee(id=UUID('00000000-0000-0000-0000-000000000002'), name='Макар', taskcount=2),
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
    assignee = assignee_service_with_repo.get_assignee_by_id(UUID('00000000-0000-0000-0000-000000000001'))
    assert assignee.name == 'Павел'


def test_get_assignee_by_invalid_id(assignee_service_with_repo):
    with pytest.raises(HTTPException):
        assignee_service_with_repo.get_assignee_by_id(UUID('invalid_id'))


def test_create_assignee(assignee_service_with_repo):
    new_assignee = assignee_service_with_repo.create_assignee(name='Новый сотрудник')
    assert new_assignee.name == 'Новый сотрудник'
    assert new_assignee.taskcount == 0


def test_update_assignee(assignee_service_with_repo):
    updated_assignee = assignee_service_with_repo.update_assignee(id=UUID('00000000-0000-0000-0000-000000000001'))
    assert updated_assignee.taskcount == 2


def test_update_assignee_with_invalid_id(assignee_service_with_repo):
    with pytest.raises(HTTPException):
        assignee_service_with_repo.update_assignee(id=UUID('invalid_id'))
