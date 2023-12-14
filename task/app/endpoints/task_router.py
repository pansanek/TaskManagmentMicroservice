import asyncio
import json
from typing import List
from uuid import UUID

import httpx
import requests
from fastapi import APIRouter, Depends, HTTPException, Security, status
import webbrowser
from app.models.create_task_request import CreateTaskRequest
from app.services.task_service import TaskService
from app.models.task import Task

from fastapi.responses import HTMLResponse
from app.rabbitmq import process_created_task


from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID
import requests
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from starlette.requests import Request
from starlette.responses import RedirectResponse

host_ip="192.168.1.100"
keycloak_authorization_url = f"http://{host_ip}:8080/realms/myrealm/protocol/openid-connect/auth"
keycloak_token_url = f"http://{host_ip}:8080/realms/myrealm/protocol/openid-connect/token"
keycloak_client_id = "myclient"
keycloak_client_secret = f"7EEuCHQvc8eQ92zTQJvFuWelkS4tpBP1"
task_router = APIRouter(prefix='/tasks', tags=['Tasks'])
user_role="Not authorized"
@task_router.get("/login")
async def login(request: Request):
    # Manually specify redirect_uri and state
    custom_redirect_uri = f"http://{host_ip}:80/api/tasks/callback"
    custom_state = "your_custom_state"

    # Construct the authorization URL with the specified parameters
    authorization_url = (f"{keycloak_authorization_url}?response_type=code&client_id={keycloak_client_id}&redirect_uri="
                         f"{custom_redirect_uri}&state={custom_state}&client_secret={keycloak_client_secret}&"
                         f"scope=openid profile")

    # Redirect the user to the authorization URL
    return RedirectResponse(url=authorization_url)

@task_router.get("/callback")
async def callback(request: Request):
    print(request.json())
    code = request.query_params.get("code")
    token = get_token(code)
    print(token)
    roles = get_user_info(token)
    print(roles)
    if "Viewer" in roles["realm_access"]["roles"]:
        user_role = "Viewer"
        return f"Authorized! Your role is:{user_role}"
    elif "Creator" in roles["realm_access"]["roles"]:
        user_role = "Creator"
        return f"Authorized! Your role is: {user_role}"
    return "Not authorized"

def get_token(code: str):
    token_url = f"http://{host_ip}:8080/realms/myrealm/protocol/openid-connect/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": keycloak_client_id,
        "client_secret": keycloak_client_secret,
        "code": code,
        "scope": "openid profile email roles",
        "redirect_uri": f"http://{host_ip}:80/api/tasks/callback"
    }
    response = requests.post(token_url, data=data)
    print(response)
    return response.json()['access_token']

def get_user_info(token: str):
    url = f"http://{host_ip}:8080/realms/myrealm/protocol/openid-connect/userinfo"
    headers = {
        "Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    print(response)
    return response.json()



@task_router.get('/')
def get_tasks(task_service: TaskService = Depends(TaskService)) -> list[Task]:
    if "Viewer" == user_role:
        return task_service.get_tasks()
    elif "Creator" ==user_role:
        return task_service.get_tasks()
    raise HTTPException(status_code=403, detail=f"{user_role}")



@task_router.post('/')
def create_task(
        task_info: CreateTaskRequest,
        task_service: TaskService = Depends(TaskService),
        current_user: dict = Depends(get_user_info)
) -> Task:
    if "Creator" not in current_user["realm_access"]["roles"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    try:
        task = task_service.create_task(task_info.id, task_info.title, task_info.description, task_info.due_date,
                                        task_info.assignee_id)
        # asyncio.run(send_assignee_update_message(task_info.assignee_id))
        return task.dict()
    except KeyError:
        raise HTTPException(400, f'Task with title={task_info.title} already exists')


@task_router.post('/{id}/start')
def start_task(id: UUID, task_service: TaskService = Depends(TaskService),
               current_user: dict = Depends(get_user_info)
               ) -> Task:
    if "Creator" not in current_user["realm_access"]["roles"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    try:
        task = task_service.start_task(id)
        return task.dict()
    except KeyError:
        raise HTTPException(404, f'Task with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Task with id={id} can\'t be started')


@task_router.post('/{id}/complete')
def complete_task(id: UUID, task_service: TaskService = Depends(TaskService),
                  current_user: dict = Depends(get_user_info)
                  ) -> Task:
    if "Creator" not in current_user["realm_access"]["roles"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    try:
        task = task_service.complete_task(id)
        return task.dict()
    except KeyError:
        raise HTTPException(404, f'Task with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Task with id={id} can\'t be completed')


@task_router.post('/{id}/cancel')
def cancel_task(id: UUID, task_service: TaskService = Depends(TaskService),
                current_user: dict = Depends(get_user_info)
                ) -> Task:
    if "Creator" not in current_user["realm_access"]["roles"]:
        raise HTTPException(status_code=403, detail="Permission denied")
    try:
        task = task_service.cancel_task(id)
        return task.dict()
    except KeyError:
        raise HTTPException(404, f'Task with id={id} not found')
    except ValueError:
        raise HTTPException(400, f'Task with id={id} can\'t be canceled')


