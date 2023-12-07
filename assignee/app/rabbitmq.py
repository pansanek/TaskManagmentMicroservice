import json
import traceback
from asyncio import AbstractEventLoop
from aio_pika.abc import AbstractRobustConnection
from aio_pika import connect_robust, IncomingMessage

from app.repositories.assignee_repo import AssigneeRepo
from app.services.assignee_service import AssigneeService
from app.settings import settings



async def process_assignee_update(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        assignee_id = data['assignee_id']

        assignee_service = AssigneeService(AssigneeRepo())
        assignee_service.update_assignee(assignee_id)
    except:
        traceback.print_exc()
    finally:
        await msg.ack()



async def consume_assignee_updates(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    assignee_update_queue = await channel.declare_queue('potemkin_assignee_update_queue', durable=True)

    await assignee_update_queue.consume(process_assignee_update)
    print('Started RabbitMQ consuming for Assignee updates...')

    return connection
