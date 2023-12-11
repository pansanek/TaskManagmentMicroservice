import asyncio
from typing import List
from uuid import UUID

import httpx
from fastapi import APIRouter, Depends, HTTPException, Security, status

from app.models.create_task_request import CreateTaskRequest
from app.services.task_service import TaskService
from app.models.task import Task

from app.rabbitmq import process_created_task

from app.rabbitmq import send_assignee_update_message
from jose import JWTError, jwt
from keycloak import KeycloakOpenID
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer

task_router = APIRouter(prefix='/tasks', tags=['Tasks'])

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="http://localhost:8080/realms/myrealm/protocol/openid-connect/token",
    scopes={"openid": "Read data with openid scope"})

async def get_user_info(token: str = Depends(oauth2_scheme)):
    try:
        decoded_token = jwt.decode(token,
                                   algorithms=["RS256"])
        user_info = {
            "sub": decoded_token.get("sub"),
            "username": decoded_token.get("preferred_username"),
            "email": decoded_token.get("email"),
            "roles": decoded_token.get("realm_access", {}).get("roles", [])
        }
        return user_info
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


# Example route that requires authentication
@task_router.get("/secure-data")
async def secure_data(current_user: dict = Depends(oauth2_scheme)):
    return {"message": "You have access to secure data!", "user": current_user}


# Пример использования декоратора в вашем коде
@task_router.get('/')
def get_tasks(task_service: TaskService = Depends(TaskService),
              current_user: dict = Depends(get_user_info)) -> list[Task]:
    if "myuser" not in current_user["roles"]:
        raise HTTPException(status_code=403, detail="Permission denied, user must have 'admin' role")
    return task_service.get_tasks()


@task_router.post('/')
def create_task(
        task_info: CreateTaskRequest,
        task_service: TaskService = Depends(TaskService)
) -> Task:
    try:
        task = task_service.create_task(task_info.id, task_info.title, task_info.description, task_info.due_date,
                                        task_info.assignee_id)
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
