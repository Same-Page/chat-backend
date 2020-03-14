import json
import logging

import boto3

from cfg import is_local, redis_client
import common


def clean_dead_connections(room_id, dead_connections):
    # Remove connection from room data
    # But not removing from user or connection table because might be too slow?
    # TODO: enforce how many connections a user can have, similar to MAX_USER_CONNECTION
    # but not per room, it's for total
    if len(dead_connections) > 0:
        print(f'[{room_id}] found dead connections: {len(dead_connections)}')

        room = common.get_room(room_id)
        users = room['users']
        gone_user_ids = []

        for user in users:
            user['connections'] = [connection_id for connection_id in user['connections']
                                   if connection_id not in dead_connections]
            if len(user['connections']) == 0:
                gone_user_ids.append(user['id'])

        room['users'] = [u for u in users if u['id'] not in gone_user_ids]

        redis_client.set(room_id, json.dumps(room))


def lambda_handler(event, context, send_message_to_socket=None):
    data = json.loads(event['Records'][0]['Sns']['Message'])
    room_id = data['room_id']
    message = data['message']
    endpoint_url = data['endpoint_url']
    payload = json.dumps(message).encode('utf-8')

    room = common.get_room(room_id)
    users = room['users']

    dead_connections = []

    for user in users:
        for connection_id in user['connections']:
            try:
                if is_local:
                    # Note: the local shim is not very accurate
                    # exception or result won't be returned here if happened
                    # in coroutine
                    resp = send_message_to_socket(connection_id, payload)
                else:
                    gatewayapi = boto3.client(
                        "apigatewaymanagementapi", endpoint_url=endpoint_url)
                    resp = gatewayapi.post_to_connection(
                        ConnectionId=connection_id, Data=payload)
            except Exception as e:
                # some connections are dropped without notice, they raise
                # exception here, we should remove these dead connections
                dead_connections.append(connection_id)
                logging.exception(
                    f'Room [{room_id}] failed to send message to connection {connection_id}')

    clean_dead_connections(room_id, dead_connections)

    return {
        'statusCode': 200,
        'body': json.dumps(f'[{room_id}] broadcast done, found dead connections: {len(dead_connections)}')
    }
