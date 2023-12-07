from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.models.create_assignee_request import CreateAssigneeRequest
from app.services.assignee_service import AssigneeService
from app.models.assignee import Assignee

assignee_router = APIRouter(prefix='/assignees', tags=['Assignees'])

@assignee_router.get('/')
def get_assignees(assignee_service: AssigneeService = Depends(AssigneeService)) -> list[Assignee]:
    return assignee_service.get_assignees()

@assignee_router.post('/')
def create_assignee(
    assignee_info: CreateAssigneeRequest,
    assignee_service: AssigneeService = Depends(AssigneeService)
) -> Assignee:
    try:
        assignee = assignee_service.create_assignee(assignee_info.name)
        return assignee.dict()
    except KeyError:
        raise HTTPException(400, f'Assignee with name={assignee_info.name} already exists')

@assignee_router.get('/{id}')
def get_assignee_by_id(id: int, assignee_service: AssigneeService = Depends(AssigneeService)) -> Assignee:
    try:
        assignee = assignee_service.get_assignee_by_id(id)
        return assignee.dict()
    except KeyError:
        raise HTTPException(404, f'Assignee with id={id} not found')

@assignee_router.put('/{id}')
def update_assignee(
    id: int,
    assignee_service: AssigneeService = Depends(AssigneeService)
) -> Assignee:
    try:
        assignee = assignee_service.update_assignee(id)
        return assignee.dict()
    except KeyError:
        raise HTTPException(404, f'Assignee with id={id} not found')
