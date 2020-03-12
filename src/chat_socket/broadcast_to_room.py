import json
import logging

import boto3
import redis

from cfg import REDIS_URL


redis_client = redis.Redis.from_url(REDIS_URL)


def lambda_handler(event, context):
    data = json.loads(event['Records'][0]['Sns']['Message'])
    room = data['room']
    message = data['message']
    endpoint_url = data['endpoint_url']

    payload = json.dumps(message).encode('utf-8')

    gatewayapi = boto3.client(
        "apigatewaymanagementapi", endpoint_url=endpoint_url)

    users = room['users']
    lost_connection = False
    gone_user_ids = []
    for user in users:
        connections_to_be_removed = []
        for connection_id in user['connections']:
            try:
                resp = gatewayapi.post_to_connection(
                    ConnectionId=connection_id, Data=payload)
            except:
                connections_to_be_removed.append(connection_id)
                lost_connection = True
                logging.error(
                    f'Room [{room["id"]}] failed to send message to connection {connection_id}')
        user['connections'] = [connection_id for connection_id in user['connections']
                               if connection_id not in connections_to_be_removed]
        if len(user['connections']) == 0:
            gone_user_ids.append(user['id'])
    room['users'] = [u for u in users if u['id'] not in gone_user_ids]
    if lost_connection:
        # Remove connection from room data
        # But not removing from user or connection table because might be too slow?
        # TODO: then set timeout on use and connection data may help
        redis_client.set(room['id'], json.dumps(room))

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
