import json

from common import get_room_messages

res = json.dumps(get_room_messages('news'))

s = len(res.encode('utf-8'))/1024
print(s)
