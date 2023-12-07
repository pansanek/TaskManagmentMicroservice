import asyncio
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.models.create_task_request import CreateTaskRequest
from app.services.task_service import TaskService
from app.models.task import Task

from app.rabbitmq import process_created_task

from app.rabbitmq import send_assignee_update_message

task_router = APIRouter(prefix='/tasks', tags=['Tasks'])

@task_router.get('/')
def get_tasks(task_service: TaskService = Depends(TaskService)) -> list[Task]:
    return task_service.get_tasks()

@task_router.post('/')
def create_task(
    task_info: CreateTaskRequest,
    task_service: TaskService = Depends(TaskService)
) -> Task:
    try:
        task = task_service.create_task(task_info.id,task_info.title, task_info.description, task_info.due_date, task_info.assignee_id)
        asyncio.run(send_assignee_update_message(task_info.assignee_id))
        return task.dict()
    except KeyError:
        raise HTTPException(400, f'Task with title={task_info.title} already exists')

@task_router.post('/{id}/start')
def start_task(id: UUID, task_service: TaskService = Depends(TaskService)) -> Task:
    try:
        task = task_service.start_task(id)
        return task.dict()
    except KeyError:
        raise HTTPException(404, f'Task with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Task with id={id} can\'t be started')

@task_router.post('/{id}/complete')
def complete_task(id: UUID, task_service: TaskService = Depends(TaskService)) -> Task:
    try:
        task = task_service.complete_task(id)
        return task.dict()
    except KeyError:
        raise HTTPException(404, f'Task with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Task with id={id} can\'t be completed')

@task_router.post('/{id}/cancel')
def cancel_task(id: UUID, task_service: TaskService = Depends(TaskService)) -> Task:
    try:
        task = task_service.cancel_task(id)
        return task.dict()
    except KeyError:
        raise HTTPException(404, f'Task with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Task with id={id} can\'t be canceled')
