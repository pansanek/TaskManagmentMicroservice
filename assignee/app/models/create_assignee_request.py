from pydantic import BaseModel
from datetime import datetime

class CreateAssigneeRequest(BaseModel):
    name: str