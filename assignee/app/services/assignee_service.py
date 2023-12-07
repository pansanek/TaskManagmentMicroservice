from uuid import UUID

from fastapi import Depends

from app.models.assignee import Assignee
from app.repositories.assignee_repo import AssigneeRepo


class AssigneeService:
    assignee_repo: AssigneeRepo

    def __init__(self, assignee_repo: AssigneeRepo = Depends(AssigneeRepo)) -> None:
        self.assignee_repo = assignee_repo

    def get_assignees(self) -> list[Assignee]:
        return self.assignee_repo.get_assignees()

    def get_assignee_by_id(self, id: UUID) -> Assignee:
        return self.assignee_repo.get_assignee_by_id(id)

    def create_assignee(self, name: str) -> Assignee:
        return self.assignee_repo.create_assignee(name)

    def update_assignee(self, id:UUID) -> Assignee:
        return self.assignee_repo.update_assignee(id)
