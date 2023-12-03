import json
import traceback
from asyncio import AbstractEventLoop
from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, IncomingMessage

from task.app.settings import settings
from task.app.services.task_service import TaskService  # Импортируем ваш сервис управления задачами
from task.app.repositories.task_repo import TaskRepo  # Импортируем ваш репозиторий для задач

async def process_created_task(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        TaskService(TaskRepo()).create_task(
            data['title'], data['description'], data['due_date'], data['assignee'])
    except:
        traceback.print_exc()
    finally:
        await msg.ack()

async def process_started_task(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        TaskService(TaskRepo()).start_task(data['id'])
    except:
        traceback.print_exc()
    finally:
        await msg.ack()

async def consume_tasks(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    task_created_queue = await channel.declare_queue('potemkin_task_created_queue', durable=True)
    task_started_queue = await channel.declare_queue('potemkin_task_started_queue', durable=True)

    await task_created_queue.consume(process_created_task)
    await task_started_queue.consume(process_started_task)
    print('Started RabbitMQ consuming for Task Management...')

    return connection

