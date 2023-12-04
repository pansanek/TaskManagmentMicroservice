import asyncio

from fastapi import FastAPI

from app import rabbitmq
from app.endpoints.task_router import task_router

app = FastAPI(title='Task Service')


@app.on_event('startup')
def startup():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(rabbitmq.consume_tasks(loop))

app.include_router(task_router,prefix='/api')