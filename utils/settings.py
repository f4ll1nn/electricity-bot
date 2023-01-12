from .telegram_token import token, user_id
LOCAL = False

#IP = '127.0.0.1'
if LOCAL:
    IP = '127.0.0.1'
else:
    IP = '78.140.129.200'
PORT = 6786
TIMEOUT = 20

LOCAL_IP = '127.0.0.1:5555'

TELEGRAM_TOKEN = token
TELEGRAM_USER_ID = user_id
