import pytest
from uuid import UUID

from app.models.assignee import Assignee
from app.repositories.assignee_repo import AssigneeRepo

# Фикстура для создания репозитория
@pytest.fixture()
def assignee_repo() -> AssigneeRepo:
    repo = AssigneeRepo()
    return repo

# Фикстура с тестовыми данными
@pytest.fixture(scope='session')
def test_assignees() -> list[Assignee]:
    return [
        Assignee(id=1, name='Павел', taskcount=0),
        Assignee(id=2, name='Макар', taskcount=0)
    ]

# Тест для проверки пустого списка
def test_empty_list(assignee_repo: AssigneeRepo) -> None:
    assert assignee_repo.get_assignees() == []

# Тест для проверки получения всех задач
def test_get_assignees(test_assignees: list[Assignee], assignee_repo: AssigneeRepo) -> None:
    # Добавляем тестовые данные в репозиторий
    assignees = test_assignees
    for assignee in assignees:
        assignee_repo.create_assignee(assignee.name)

    # Получаем список задач из репозитория и сравниваем с тестовыми данными
    assert assignee_repo.get_assignees() == assignees

# Тест для проверки создания новой задачи
def test_create_assignee(assignee_repo: AssigneeRepo) -> None:
    # Создаем нового исполнителя
    new_assignee_name = 'Новый исполнитель'
    new_assignee = assignee_repo.create_assignee(new_assignee_name)

    # Проверяем, что новый исполнитель добавлен в репозиторий
    assert new_assignee in assignee_repo.get_assignees()

# Тест для проверки получения исполнителя по ID
def test_get_assignee_by_id(test_assignees: list[Assignee], assignee_repo: AssigneeRepo) -> None:
    # Добавляем тестовые данные в репозиторий
    assignees = test_assignees
    for assignee in assignees:
        assignee_repo.create_assignee(assignee.name)

    # Выбираем случайного исполнителя из тестовых данных
    random_assignee = assignees[1]

    # Получаем исполнителя из репозитория по ID и сравниваем с выбранным исполнителем
    assert assignee_repo.get_assignee_by_id(random_assignee.id) == random_assignee
