import json
import traceback
from asyncio import AbstractEventLoop
from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, IncomingMessage

from assignee.app.repositories.assignee_repo import AssigneeRepo
from assignee.app.services.assignee_service import AssigneeService
from task.app.settings import settings


async def process_created_assignee(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        AssigneeService(AssigneeRepo()).create_assignee(data['name'])
    except:
        traceback.print_exc()
        await msg.ack()


async def process_assignee_update(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        assignee_id = data['assignee_id']

        assignee_service = AssigneeService(AssigneeRepo())
        assignee = assignee_service.get_assignee_by_id(assignee_id)
        assignee.taskcount += 1
        assignee_service.update_assignee(assignee)
    except:
        traceback.print_exc()
    finally:
        await msg.ack()


async def consume_assignees(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    assignee_created_queue = await channel.declare_queue('potemkin_assignee_created_queue', durable=True)

    await assignee_created_queue.consume(process_created_assignee)
    print('Started RabbitMQ consuming for assignees...')

    return connection

async def consume_assignee_updates(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    assignee_update_queue = await channel.declare_queue('potemkin_assignee_update_queue', durable=True)

    await assignee_update_queue.consume(process_assignee_update)
    print('Started RabbitMQ consuming for Assignee updates...')

    return connection
