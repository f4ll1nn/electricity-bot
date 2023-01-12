import time

import telebot
import zmq
import datetime
from .settings import TELEGRAM_TOKEN, TELEGRAM_USER_ID, LOCAL_IP
from string import Formatter
import telegram
import asyncio

bot = telegram.Bot(token=TELEGRAM_TOKEN)
print(TELEGRAM_TOKEN, TELEGRAM_USER_ID)

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

async def send_turn_on():
    message = "Ура, світло включили\nСвітла не було протягом " + str_delta(int(passed_time.total_seconds()))
    print(message)
    return await bot.send_message(TELEGRAM_USER_ID, message)

async def send_turn_off():
    message = "Сука, світло офнули\nСвітло було протягом " + str_delta(int(passed_time.total_seconds()))
    print(message)
    return await bot.send_message(TELEGRAM_USER_ID, message)

async def check_status():
    global status, passed_time, last_status_change_time
    status = get_status()
    while True:
        new_status = get_status()
        if new_status!= status:
            passed_time = datetime.datetime.now() - last_status_change_time
            last_status_change_time = datetime.datetime.now()
            status = new_status
            if new_status == "True":
                await send_turn_on()
            else:
                await send_turn_off()

def run():
    asyncio.run(check_status())

if __name__ == '__main__':
    run()