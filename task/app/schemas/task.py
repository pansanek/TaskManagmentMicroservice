from sqlalchemy import Column, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID

from task.app.schemas.base_schema import Base
from task.app.models.task import TaskStatuses  # Импортируем предполагаемую модель статусов задач


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(UUID(as_uuid=True), primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=False)
    status = Column(Enum(TaskStatuses), nullable=False)
    assignee_id = Column(int, nullable=True)  # Предположим, что здесь будет имя назначенного исполнителя задачи
