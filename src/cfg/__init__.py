import os
env = os.environ.get('sp-env', 'staging')
print(f'NOTE: running env {env}')

is_local = env.lower() == 'local'
is_local = True

API_URL = "https://api-v2.yiyechat.com"
CHAT_SOCKET_DOMAIN = "chat-v6.yiyechat.com"
REDIS_URL = 'redis://same-page-cache.1brzf1.0001.apse1.cache.amazonaws.com:6379'
CHAT_HISTORY_REDIS_URL = 'redis://sp-chat-history.1brzf1.0001.apse1.cache.amazonaws.com:6379'

MAX_ROOM_HISTORY = 30

if is_local:
    # prod proxy
    # CHAT_HISTORY_REDIS_URL = 'redis://13.229.251.12:7617'
    # REDIS_URL = 'redis://13.229.251.12:7618'
    REDIS_URL = CHAT_HISTORY_REDIS_URL = 'redis://0.0.0.0:6379'
