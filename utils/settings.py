from .private_settings import token, user_id, mongo_connect_string, server_ip
LOCAL = False
MONGO = True

IDS = [user_id]

if LOCAL:
    IP = '127.0.0.1'
else:
    IP = server_ip
PORT = 6786

TIMEOUT = 20

LOCAL_IP = '127.0.0.1:5555'

TELEGRAM_TOKEN = token

MONGO_CONNECT_STRING = mongo_connect_string