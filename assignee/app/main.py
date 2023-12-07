import asyncio

from fastapi import FastAPI

from app import rabbitmq
from app.endpoints.assignee_router import assignee_router

app = FastAPI(title='Assignee Service')


@app.on_event('startup')
def startup():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(rabbitmq.consume_assignee_updates(loop))  # Добавлен запуск обработчика обновлений исполнителей
app.include_router(assignee_router,prefix='/api')