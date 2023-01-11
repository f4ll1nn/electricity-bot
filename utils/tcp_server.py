import asyncio
import datetime
import threading

timestamp = datetime.datetime.now()
connected = False
port = 6789

class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        global connected
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport
        connected = True

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
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: EchoServerProtocol(),
        '78.140.129.200', port)

    async with server:
        await server.serve_forever()


async def check_connection():
    global connected
    while True:
        if connected:
            if datetime.datetime.now() - timestamp > datetime.timedelta(seconds=10):
                print("Connection timed out")
                connected = False
                await asyncio.sleep(1)

async def print_status():
    while True:
        print(connected)
        await asyncio.sleep(1)


if __name__ == '__main__':
    port = int(input("Enter port: "))
    thread1 = threading.Thread(target=asyncio.run, args=(check_connection(),))
    thread1.start()
    thread2 = threading.Thread(target=asyncio.run, args=(main(),))
    thread2.start()
    thread3 = threading.Thread(target=asyncio.run, args=(print_status(),))
    thread3.start()
