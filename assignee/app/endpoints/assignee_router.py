from uuid import UUID

import prometheus_client
from fastapi import APIRouter, Depends, HTTPException
from fastapi import Response

from app.models.create_assignee_request import CreateAssigneeRequest
from app.services.assignee_service import AssigneeService
from app.models.assignee import Assignee

assignee_router = APIRouter(prefix='/assignees', tags=['Assignees'])
metrics_router = APIRouter(tags=['Metrics'])
get_assignee_count = prometheus_client.Counter(
    "get_assignee_count",
    "Number of get requests"
)
created_assignee_count = prometheus_client.Counter(
    "created_assignee_count",
    "Number of created assignees"
)
update_assignee_count = prometheus_client.Counter(
    "update_assignee_count",
    "Number of updated assignees"
)
created_assignee_count_failed = prometheus_client.Counter(
    "created_assignee_count_failed",
    "Number of failed created assignees"
)
update_assignee_count_failed = prometheus_client.Counter(
    "update_assignee_count_failed",
    "Number of failed updated assignees"
)


@assignee_router.get('/')
def get_assignees(assignee_service: AssigneeService = Depends(AssigneeService)) -> list[Assignee]:
    get_assignee_count.inc(1)
    return assignee_service.get_assignees()

@assignee_router.post('/')
def create_assignee(
    assignee_info: CreateAssigneeRequest,
    assignee_service: AssigneeService = Depends(AssigneeService)
) -> Assignee:
    try:
        assignee = assignee_service.create_assignee(assignee_info.name)
        created_assignee_count.inc(1)
        return assignee.dict()
    except KeyError:
        created_assignee_count_failed.inc(1)
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
        update_assignee_count.inc(1)
        return assignee.dict()
    except KeyError:
        update_assignee_count_failed.inc(1)
        raise HTTPException(404, f'Assignee with id={id} not found')
@metrics_router.get('/metrics')
def get_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest()
    )