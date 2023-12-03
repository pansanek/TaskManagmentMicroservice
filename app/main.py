from fastapi import FastAPI
from app.endpoints.task_router import task_router

app = FastAPI(title='Task Service')

app.include_router(task_router,prefix='/api')