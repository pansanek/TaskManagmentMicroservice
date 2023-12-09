import pytest
from uuid import UUID

from app.models.assignee import Assignee
from app.repositories.assignee_repo import AssigneeRepo


@pytest.fixture()
def assignee_repo() -> AssigneeRepo:
    repo = AssigneeRepo()
    return repo


@pytest.fixture(scope='session')
def test_assignees() -> list[Assignee]:
    return [
        Assignee(id=1, name='Павел', taskcount=1),
        Assignee(id=2, name='Макар', taskcount=1)
    ]


def test_get_assignees(test_assignees: list[Assignee], assignee_repo: AssigneeRepo) -> None:
    assert assignee_repo.get_assignees() == [
        Assignee(id=1, name='Павел', taskcount=1),
        Assignee(id=2, name='Макар', taskcount=1)
    ]


def test_create_assignee(assignee_repo: AssigneeRepo) -> None:
    new_assignee_name = 'Новыйисполнитель'
    new_assignee = assignee_repo.create_assignee(new_assignee_name)

    assert new_assignee in assignee_repo.get_assignees()


def test_get_assignee_by_id(test_assignees: list[Assignee], assignee_repo: AssigneeRepo) -> None:
    assignees = test_assignees
    for assignee in assignees:
        assignee_repo.create_assignee(assignee.name)

    random_assignee = assignees[1]

    assert assignee_repo.get_assignee_by_id(random_assignee.id) == random_assignee