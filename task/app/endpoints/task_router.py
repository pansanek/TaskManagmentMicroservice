import asyncio
import json
from typing import List
from uuid import UUID

import httpx
import requests
from fastapi import APIRouter, Depends, HTTPException, Security, status

from app.models.create_task_request import CreateTaskRequest
from app.services.task_service import TaskService
from app.models.task import Task

from app.rabbitmq import process_created_task


from fastapi.security import  OAuth2PasswordBearer
from keycloak import KeycloakOpenID

task_router = APIRouter(prefix='/tasks', tags=['Tasks'])

# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl="http://keycloak:8080/realms/myrealm/protocol/openid-connect/token",
#     scopes={"openid": "Read data with openid scope"})

def get_user_info(username: str,password :str):
    token_url = "http://keycloak:8080/realms/myrealm/protocol/openid-connect/token"
    data = {
        "grant_type": "password",
        "client_id": "myclient",
        "client_secret": "7EEuCHQvc8eQ92zTQJvFuWelkS4tpBP1",
        "username": username,
        "password": password,
        "scope": "openid"
    }
    response = requests.post(token_url, data=data)

    url = "http://keycloak:8080/realms/myrealm/protocol/openid-connect/userinfo"
    headers = {
        "Authorization": f"Bearer {response.json()['access_token']}"}
    try:
        response = requests.get(url,headers=headers)
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"{str(e)}")
    # keycloak_openid = KeycloakOpenID(server_url="http://keycloak:8080/realms/myrealm/",
    #                                  client_id="myclient",
    #                                  realm_name="myrealm",
    #                                  client_secret_key="7EEuCHQvc8eQ92zTQJvFuWelkS4tpBP1",
    #                                  )
    # config_well_known = keycloak_openid.well_known()
    # userinfo = keycloak_openid.userinfo(token)
    # print(userinfo)

# @task_router.get("/secure-data")
# def secure_data(current_user: dict = Depends(oauth2_scheme)):
#     return {"message": "You have access to secure data!", "user": current_user}


@task_router.get('/')
def get_tasks(task_service: TaskService = Depends(TaskService),
              current_user: dict = Depends(get_user_info)) -> list[Task]:
    print(current_user["realm_access"]["roles"])
    if "Viewer" in current_user["realm_access"]["roles"]:
        return task_service.get_tasks()
    elif "Creator" in current_user["realm_access"]["roles"]:
        return task_service.get_tasks()
    raise HTTPException(status_code=403, detail="Permission denied")



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
