import pytest
from uuid import UUID, uuid4
from app.models.assignee import Assignee
from app.repositories.assignee_repo import AssigneeRepo, AssigneeService


@pytest.fixture(scope='function')
def assignee_repo():
    return AssigneeRepo(clear=True)


@pytest.fixture(scope='function')
def assignee_service(assignee_repo):
    return AssigneeService(assignee_repo)


def test_empty_list(assignee_repo):
    assert assignee_repo.get_assignees() == []


def test_create_assignee(assignee_repo):
    initial_assignees = assignee_repo.get_assignees()
    new_assignee = assignee_repo.create_assignee(name='John Doe')
    updated_assignees = assignee_repo.get_assignees()

    assert len(updated_assignees) == len(initial_assignees) + 1
    assert new_assignee in updated_assignees


def test_create_assignee_duplicate(assignee_repo):
    assignee_repo.create_assignee(name='Joh Doe')

    with pytest.raises(KeyError):
        assignee_repo.create_assignee(name='John Doe')


def test_get_assignee_by_id(assignee_repo):
    new_assignee = assignee_repo.create_assignee(name='John Doe')
    retrieved_assignee = assignee_repo.get_assignee_by_id(new_assignee.id)

    assert retrieved_assignee == new_assignee


def test_get_assignee_by_id_error(assignee_repo):
    with pytest.raises(KeyError):
        assignee_repo.get_assignee_by_id(UUID('some-invalid-uuid'))


def test_update_assignee(assignee_repo):
    new_assignee = assignee_repo.create_assignee(name='John Doe')
    updated_assignee = assignee_repo.update_assignee(id=new_assignee.id)

    assert updated_assignee.taskcount == new_assignee.taskcount + 1


# Test the AssigneeService

def test_service_get_assignees(assignee_service):
    assignees = assignee_service.get_assignees()
    assert assignees == []


def test_service_create_assignee(assignee_service):
    new_assignee = assignee_service.create_assignee(name='Jane Doe')
    assert new_assignee.name == 'Jane Doe'


def test_service_update_assignee(assignee_service):
    new_assignee = assignee_service.create_assignee(name='Jane Doe')
    updated_assignee = assignee_service.update_assignee(id=new_assignee.id)

    assert updated_assignee.taskcount == new_assignee.taskcount + 1
