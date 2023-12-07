import pytest
from uuid import UUID

from app.services.assignee_service import AssigneeService
from app.repositories.assignee_repo import AssigneeRepo

@pytest.fixture(scope='session')
def assignee_service() -> AssigneeService:
    return AssigneeService(AssigneeRepo(clear=True))


def test_empty_assignees(assignee_service: AssigneeService) -> None:
    assert assignee_service.get_assignees() == []


def test_create_assignee(assignee_service: AssigneeService) -> None:
    name = "John"
    assignee = assignee_service.create_assignee(name)
    assert assignee.name == name


def test_get_assignee_by_id(assignee_service: AssigneeService) -> None:
    created_assignee = assignee_service.create_assignee("Alice")
    retrieved_assignee = assignee_service.get_assignee_by_id(created_assignee.id)
    assert retrieved_assignee == created_assignee


def test_update_assignee(assignee_service: AssigneeService) -> None:
    created_assignee = assignee_service.create_assignee("Bob")
    updated_assignee = assignee_service.update_assignee(created_assignee.id)
    assert updated_assignee.taskcount == created_assignee.taskcount


