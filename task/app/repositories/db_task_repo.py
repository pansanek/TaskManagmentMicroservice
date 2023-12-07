import traceback
from uuid import UUID
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.task import Task
from app.schemas.task import Task as DBTask


class TaskRepo:
    db: Session

    def __init__(self) -> None:
        self.db = next(get_db())

    def _map_to_model(self, task: DBTask) -> Task:
        result = Task.from_orm(task)
        # if task.assignee is not 0:
        #     result.assignee = self.assignee_repo.get_assignee_by_id(
        #         task.assignee)

        return result

    def _map_to_schema(self, task: Task) -> DBTask:
        data = dict(task)
        del data['assignee_id']
        data['assignee_id'] = task.assignee_id if task.assignee_id is not 0 else 0
        result = DBTask(**data)

        return result

    def get_tasks(self) -> list[Task]:
        tasks = []
        for t in self.db.query(DBTask).all():
            tasks.append(self._map_to_model(t))
        return tasks

    def get_task_by_id(self, id: UUID) -> Task:
        task = self.db \
            .query(DBTask) \
            .filter(DBTask.id == id) \
            .first()

        if task is None:
            raise KeyError
        return self._map_to_model(task)

    def create_task(self, task: Task) -> Task:
        try:
            db_task = self._map_to_schema(task)
            self.db.add(db_task)
            self.db.commit()
            return self._map_to_model(db_task)
        except:
            traceback.print_exc()
            raise KeyError

    def set_status(self, task: Task) -> Task:
        db_task = self.db.query(DBTask).filter(
            DBTask.id == task.id).first()
        db_task.status = task.status
        self.db.commit()
        return self._map_to_model(db_task)

    def start_task(self, task: Task) -> Task:
        db_task = self.db.query(DBTask).filter(
            DBTask.id == task.id).first()
        db_task.status = task.status
        self.db.commit()
        return self._map_to_model(db_task)
