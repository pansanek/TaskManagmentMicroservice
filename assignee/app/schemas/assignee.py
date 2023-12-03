from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from task.app.schemas.base_schema import Base

class Assignee(Base):
    __tablename__ = 'assignees'

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    taskcount = Column(int,nullable=False)
