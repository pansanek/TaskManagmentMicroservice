from enum import Enum
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class TaskStatuses(Enum):
    TODO = 'todo'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    CANCELED = 'canceled'

class Task(BaseModel):
    id: UUID
    title: str
    description: str
    due_date: datetime
    status: TaskStatuses
    assignee_id: int