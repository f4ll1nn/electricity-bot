import time


import zmq
import datetime
from string import Formatter
import telegram
import asyncio

from .settings import TELEGRAM_TOKEN, LOCAL_IP
from .mongo_storage import MongoStorage


bot = telegram.Bot(token=TELEGRAM_TOKEN)

status = False
passed_time = datetime.timedelta
last_status_change_time = datetime.datetime.now()

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect('tcp://' + LOCAL_IP)


def str_delta(secs_passed):
    fmt = "{H:02}:{M:02}:{S:02}"
    f = Formatter()
    hours, remainder = divmod(secs_passed, 60 * 60)
    minutes, seconds = divmod(remainder, 60)
    dict = {"H": hours, 'M': minutes, 'S': seconds}
    result = f.format(fmt, **dict)
    return result


def get_status():
    socket.send_string("status")
    status = socket.recv_string()
    return status


async def send_message(status):
    ids = mongo_storage.get_ids()
    if status == "True":
        message = "Ура, світло включили\nСвітла не було протягом "
    else:
        message = "Сука, світло офнули\nСвітло було протягом "
    for id in ids:
        await bot.send_message(chat_id=id, text=message + str_delta(int(passed_time.total_seconds())))
    return 0


async def check_status():
    global status, passed_time, last_status_change_time
    status = get_status()
    while True:
        new_status = get_status()
        if new_status != status:
            passed_time = datetime.datetime.now() - last_status_change_time
            last_status_change_time = datetime.datetime.now()
            status = new_status
            await send_message(status)


def run():
    global mongo_storage
    mongo_storage = MongoStorage()
    asyncio.run(check_status())


if __name__ == '__main__':
    run()
