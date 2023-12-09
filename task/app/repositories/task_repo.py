from datetime import datetime, timedelta
from uuid import UUID
from app.models.task import Task, TaskStatuses

tasks: list[Task] = [
    Task(
        id=UUID('00000000-0000-0000-0000-000000000011'),
        title='Создать отчет по продажам',
        description='Описание задания: Создать отчет по продажам',
        due_date=datetime.now() + timedelta(days=7),
        status=TaskStatuses.TODO,
        assignee_id=1
    ),
    Task(
        id=UUID('00000000-0000-0000-0000-000000000002'),
        title='Подготовить презентацию для клиента',
        description='Описание задания: Подготовить презентацию для клиента',
        due_date=datetime.now() + timedelta(days=5),
        status=TaskStatuses.TODO,
        assignee_id=2
    )
]


class TaskRepo:
    
    def __init__(self, clear: bool = False) -> None:
        if clear:
            tasks.clear()

    def get_tasks(self) -> list[Task]:
        return tasks

    def get_task_by_id(self, id: UUID) -> Task:
        for task in tasks:
            if task.id == id:
                return task

        raise KeyError

    def create_task(self, task: Task) -> Task:
        if len([t for t in tasks if t.id == task.id]) > 0:
            raise KeyError("Task with the same id already exists.")

        tasks.append(task)
        return task

    def set_status(self, task: Task) -> Task:
        for t in tasks:
            if t.id == task.id:
                t.status = task.status
                break

        return task
