from uuid import UUID

from pydantic import BaseModel
from datetime import datetime

class CreateTaskRequest(BaseModel):
    id: UUID
    title: str
    description: str
    due_date: datetime
    assignee_id: int