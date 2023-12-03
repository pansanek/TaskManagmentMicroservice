# app/schemas/assignee.py

from pydantic import BaseModel
from uuid import UUID

class Assignee(BaseModel):
    id: UUID
    name: str
    taskcount: int
