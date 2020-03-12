import json

from boto3 import client as boto3_client
import boto3
from boto3.dynamodb.conditions import Attr

from common import get_room

dynamodb = boto3.resource("dynamodb")

rooms_table = dynamodb.Table("rooms")


def lambda_handler(event, context):
    room_type = None
    try:
        room_type = event.get("queryStringParameters", {}).get('type')
    except:
        pass
    if room_type:
        response = rooms_table.scan(
            FilterExpression=Attr('type').eq(room_type))
    else:
        response = rooms_table.scan()
    rooms = response['Items']
    # TODO: fetching user number every time is wasteful, should cache
    for room in rooms:
        realtime_room_data = get_room(room['id'])
        if realtime_room_data:
            room['userCount'] = len(realtime_room_data['users'])
        else:
            room['userCount'] = 0

    return {
        'statusCode': 200,
        'body': json.dumps(rooms),
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'token'
        },
    }


if __name__ == "__main__":
    print(lambda_handler(None, None))
