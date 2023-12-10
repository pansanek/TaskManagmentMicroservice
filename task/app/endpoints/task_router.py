import asyncio
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

import prometheus_client

from app.models.create_task_request import CreateTaskRequest
from app.services.task_service import TaskService
from app.models.task import Task

from app.rabbitmq import process_created_task

from app.rabbitmq import send_assignee_update_message
from fastapi import Response

task_router = APIRouter(prefix='/tasks', tags=['Tasks'])
metrics_router = APIRouter(tags=['Metrics'])
get_task_count = prometheus_client.Counter(
    "get_task_count",
    "Number of get requests"
)
created_task_count = prometheus_client.Counter(
    "created_task_count",
    "Number of created tasks"
)
started_task_count = prometheus_client.Counter(
    "started_task_count",
    "Number of started tasks"
)
complete_task_count = prometheus_client.Counter(
    "complete_task_count",
    "Number of completed tasks"
)
cancel_task_count = prometheus_client.Counter(
    "cancel_task_count",
    "Number of canceled tasks"
)

created_task_count_failed = prometheus_client.Counter(
    "created_task_count_failed",
    "Number of failed created tasks"
)
started_task_count_failed = prometheus_client.Counter(
    "started_task_count_failed",
    "Number of failed started tasks"
)
complete_task_count_failed = prometheus_client.Counter(
    "complete_task_count_failed",
    "Number of failed completed tasks"
)
cancel_task_count_failed = prometheus_client.Counter(
    "cancel_task_count_failed",
    "Number of failed canceled tasks"
)
@task_router.get('/')
def get_tasks(task_service: TaskService = Depends(TaskService)) -> list[Task]:
    get_task_count.inc(1)
    return task_service.get_tasks()

@task_router.post('/')
def create_task(
    task_info: CreateTaskRequest,
    task_service: TaskService = Depends(TaskService)
) -> Task:
    try:
        task = task_service.create_task(task_info.id,task_info.title, task_info.description, task_info.due_date, task_info.assignee_id)
        asyncio.run(send_assignee_update_message(task_info.assignee_id))
        created_task_count.inc(1)
        return task.dict()
    except KeyError:
        created_task_count_failed.inc(1)
        raise HTTPException(400, f'Task with title={task_info.title} already exists')

@task_router.post('/{id}/start')
def start_task(id: UUID, task_service: TaskService = Depends(TaskService)) -> Task:
    try:
        task = task_service.start_task(id)
        started_task_count.inc(1)
        return task.dict()
    except KeyError:
        started_task_count_failed.inc(1)
        raise HTTPException(404, f'Task with id={id} not found')
    except ValueError:
        started_task_count_failed.inc(1)
        raise HTTPException(400, f'Task with id={id} can\'t be started')

@task_router.post('/{id}/complete')
def complete_task(id: UUID, task_service: TaskService = Depends(TaskService)) -> Task:
    try:
        task = task_service.complete_task(id)
        complete_task_count.inc(1)
        return task.dict()
    except KeyError:
        complete_task_count_failed.inc(1)
        raise HTTPException(404, f'Task with id={id} not found')
    except ValueError:
        complete_task_count_failed.inc(1)
        raise HTTPException(400, f'Task with id={id} can\'t be completed')

@task_router.post('/{id}/cancel')
def cancel_task(id: UUID, task_service: TaskService = Depends(TaskService)) -> Task:
    try:
        task = task_service.cancel_task(id)
        cancel_task_count.inc(1)
        return task.dict()
    except KeyError:
        cancel_task_count_failed.inc(1)
        raise HTTPException(404, f'Task with id={id} not found')
    except ValueError:
        cancel_task_count_failed.inc(1)
        raise HTTPException(400, f'Task with id={id} can\'t be canceled')

@metrics_router.get('/metrics')
def get_metrics():
    return Response(
        media_type="text/plain",
        content=prometheus_client.generate_latest()
    )