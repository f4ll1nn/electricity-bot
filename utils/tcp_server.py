import asyncio
import datetime
import threading
import zmq

from .settings import IP, PORT, TIMEOUT, LOCAL_IP

timestamp = datetime.datetime.now()
connected = False

context = zmq.Context()


def send_status():
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://' + LOCAL_IP)
    socket.send_string("set " + str(connected))
    status = socket.recv_string()
    socket.close()
    return status


class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        global connected
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport
        connected = True
        send_status()

    def data_received(self, data):
        global timestamp
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)
        timestamp = datetime.datetime.now()

        print('Close the client socket')
        self.transport.close()


async def main():
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: EchoServerProtocol(),
        IP, PORT)

    async with server:
        await server.serve_forever()


async def check_connection():
    global connected
    while True:
        if connected:
            if datetime.datetime.now() - timestamp > datetime.timedelta(seconds=TIMEOUT):
                print("Connection timed out")
                connected = False
                send_status()
        await asyncio.sleep(1)


async def print_status():
    while True:
        print(connected)
        await asyncio.sleep(1)


def run():
    thread1 = threading.Thread(target=asyncio.run, args=(check_connection(),))
    thread1.start()
    thread2 = threading.Thread(target=asyncio.run, args=(main(),))
    thread2.start()
    thread3 = threading.Thread(target=asyncio.run, args=(print_status(),))
    thread3.start()


if __name__ == '__main__':
    run()
