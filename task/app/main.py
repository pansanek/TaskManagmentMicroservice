import asyncio

from fastapi import FastAPI

from app import rabbitmq
from app.endpoints.task_router import task_router,metrics_router
import logging
from logging_loki import LokiHandler
app = FastAPI(title='Task Service')

loki_logs_handler = LokiHandler(
    url="http://loki:3100/loki/api/v1/push",
    tags={"application": "fastapi"},
    version="1",
)
logger = logging.getLogger("uvicorn.access")
logger.addHandler(loki_logs_handler)

@app.on_event('startup')
def startup():
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(rabbitmq.consume_tasks(loop))

app.include_router(task_router,prefix='/api')
app.include_router(metrics_router)