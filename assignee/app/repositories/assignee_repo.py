from uuid import UUID

from app.models.assignee import Assignee

assignees: list[Assignee] = [

]

class AssigneeRepo:

    def __init__(self, clear: bool = False) -> None:
        if clear:
            assignees.clear()

    def get_assignees(self) -> list[Assignee]:
        return assignees

    def get_assignee_by_id(self, id: int) -> Assignee:
        for assignee in assignees:
            if assignee.id == id:
                return assignee

        raise KeyError

    def create_assignee(self, name: str) -> Assignee:
        new_assignee = Assignee(id=len(assignees) + 1, name=name, taskcount=0)
        assignees.append(new_assignee)
        return new_assignee

    def update_assignee(self, id:int) -> Assignee:
        for item in assignees:
            if item.id == id:
                item.taskcount += 1
                return item

        raise KeyError
