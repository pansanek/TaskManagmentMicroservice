import json
import traceback
from asyncio import AbstractEventLoop
from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, IncomingMessage, Message

from app.settings import settings
from app.services.task_service import TaskService  # Импортируем ваш сервис управления задачами
from app.repositories.task_repo import TaskRepo  # Импортируем ваш репозиторий для задач

async def process_created_task(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        await send_assignee_update_message(data['assignee_id'])
    except:
        traceback.print_exc()
    finally:
        await msg.ack()

async def send_assignee_update_message(assignee_id: int):
    print('SENDING UPDATE')
    connection = await connect_robust(settings.amqp_url)
    channel = await connection.channel()


    message_body = json.dumps({'assignee_id': assignee_id})
    await channel.default_exchange.publish(
        Message(body=message_body.encode()),
        routing_key='potemkin_assignee_update_queue'
    )
    # Close the channel and connection
    await channel.close()
    await connection.close()



async def consume_tasks(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    task_created_queue = await channel.declare_queue('potemkin_task_created_queue', durable=True)


    await task_created_queue.consume(process_created_task)
    print('Started RabbitMQ consuming for Task Management...')

    return connection

