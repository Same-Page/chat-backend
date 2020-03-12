import json
import asyncio
from .broadcast_to_room import lambda_handler
from .local_sockets import local_sockets


def queue_message(message):
    mock_event = {
        'Records': [{
            'Sns': {
                'Message': message
            }
        }]
    }
    lambda_handler(mock_event, None,
                   send_message_to_socket=send_message_to_socket)


def send_message_to_socket(connection_id, data):
    if connection_id in local_sockets:
        print('send_message_to_socket')
        socket = local_sockets[connection_id]
        asyncio.create_task(socket.send(data.decode()))
        # asyncio.run(socket.send(data))
