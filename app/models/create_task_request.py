from pydantic import BaseModel
from datetime import datetime

class CreateTaskRequest(BaseModel):
    title: str
    description: str
    due_date: datetime
    assignee: str