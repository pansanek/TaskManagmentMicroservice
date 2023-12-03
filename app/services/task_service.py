from fastapi import Depends
from uuid import UUID
from datetime import datetime
from typing import List

from app.models.task import Task, TaskStatuses
from app.repositories.task_repo import TaskRepo


class TaskService:
    task_repo: TaskRepo
    #assignee_repo: AssigneeRepo

    def __init__(self, task_repo: TaskRepo = Depends(TaskRepo)) -> None:
        self.task_repo = task_repo
        #self.assignee_repo = AssigneeRepo()

    def get_tasks(self) -> List[Task]:
        return self.task_repo.get_tasks()

    def create_task(self, title: str, description: str, due_date: datetime, assignee: str) -> Task:
        task = Task(id=UUID(), title=title, description=description, due_date=due_date, status=TaskStatuses.TODO, assignee=assignee)
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
