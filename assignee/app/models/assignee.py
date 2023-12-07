# app/schemas/assignee.py

from pydantic import BaseModel
from uuid import UUID

class Assignee(BaseModel):
    id: int
    name: str
    taskcount: int
