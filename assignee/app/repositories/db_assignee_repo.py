import traceback
from uuid import UUID
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.assignee import Assignee
from app.schemas.assignee import Assignee as DBAssignee

class AssigneeRepo:
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())
        self.assignee_repo = AssigneeRepo()

    def _map_to_model(self, assignee: DBAssignee) -> Assignee:
        result = Assignee.from_orm(assignee)
        # Предположим, что здесь может быть логика для получения списка задач исполнителя
        # result.tasks = self.task_repo.get_tasks_for_assignee(assignee.id)
        return result

    def get_assignees(self) -> list[Assignee]:
        assignees = []
        for a in self.db.query(DBAssignee).all():
            assignees.append(self._map_to_model(a))
        return assignees

    def get_assignee_by_id(self, id: UUID) -> Assignee:
        assignee = self.db \
            .query(DBAssignee) \
            .filter(DBAssignee.id == id) \
            .first()

        if assignee is None:
            raise KeyError
        return self._map_to_model(assignee)

    def create_assignee(self, assignee: Assignee) -> Assignee:
        try:
            db_assignee = DBAssignee(**dict(assignee))
            self.db.add(db_assignee)
            self.db.commit()
            return self._map_to_model(db_assignee)
        except:
            traceback.print_exc()
            raise KeyError

    def update_assignee(self, assignee: Assignee) -> Assignee:
        try:
            db_assignee = self.db.query(DBAssignee).filter(DBAssignee.id == assignee.id).first()
            db_assignee.taskcount = assignee.taskcount
            self.db.commit()
            return assignee
        except:
            traceback.print_exc()
            raise KeyError