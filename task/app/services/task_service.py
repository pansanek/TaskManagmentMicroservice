from fastapi import Depends
from uuid import UUID
from datetime import datetime
from typing import List

from app.models.task import Task, TaskStatuses
from app.repositories.db_task_repo import TaskRepo

class TaskService:
    task_repo: TaskRepo

    def __init__(self, task_repo: TaskRepo = Depends(TaskRepo)) -> None:
        self.task_repo = task_repo


    def get_tasks(self) -> List[Task]:
        return self.task_repo.get_tasks()

    def create_task(self,task_id:UUID, title: str, description: str, due_date: datetime, assignee_id: int) -> Task:
        task = Task(id=task_id, title=title, description=description, due_date=due_date, status=TaskStatuses.TODO, assignee_id=assignee_id)
        return self.task_repo.create_task(task)

    def start_task(self, id: UUID) -> Task:
        task = self.task_repo.get_task_by_id(id)
        if task.status != TaskStatuses.TODO:
            raise ValueError("Task is not in TODO status.")

        task.status = TaskStatuses.IN_PROGRESS
        return self.task_repo.set_status(task)

    def complete_task(self, id: UUID) -> Task:
        task = self.task_repo.get_task_by_id(id)
        if task.status != TaskStatuses.IN_PROGRESS:
            raise ValueError("Task is not in progress.")

        task.status = TaskStatuses.COMPLETED
        return self.task_repo.set_status(task)

    def cancel_task(self, id: UUID) -> Task:
        task = self.task_repo.get_task_by_id(id)
        if task.status == TaskStatuses.COMPLETED:
            raise ValueError("Completed tasks cannot be canceled.")

        task.status = TaskStatuses.CANCELED
        return self.task_repo.set_status(task)

    def get_assignee_task_count(self, assignee_id: UUID) -> int:
        tasks = self.get_tasks()
        return sum(1 for task in tasks if task.assignee_id == assignee_id)

    def get_task_by_id(self, id: UUID) -> Task:
        task = self.task_repo.get_task_by_id(id)
        return task
