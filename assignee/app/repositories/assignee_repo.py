from uuid import UUID

from app.models.assignee import Assignee

assignees: list[Assignee] = [
        Assignee(id=UUID('00000000-0000-0000-0000-000000000001'), name='Павел', taskcount = 1),
        Assignee(id=UUID('00000000-0000-0000-0000-000000000002'), name='Макар', taskcount = 1)
]

class AssigneeRepo:

    def __init__(self, clear: bool = False) -> None:
        if clear:
            assignees.clear()

    def get_assignees(self) -> list[Assignee]:
        return assignees

    def get_assignee_by_id(self, id: UUID) -> Assignee:
        for assignee in assignees:
            if assignee.id == id:
                return assignee

        raise KeyError

    def create_assignee(self, name: str) -> Assignee:
        new_assignee = Assignee(id=UUID(), name=name)
        assignees.append(new_assignee)
        return new_assignee

    def update_assignee(self, id:UUID) -> Assignee:
        for item in assignees:
            if item.id == id:
                item.taskcount += 1
                return item

        raise KeyError