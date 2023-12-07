from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.schemas.base_schema import Base

class Assignee(Base):
    __tablename__ = 'assignees'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    taskcount = Column(Integer,nullable=False)
