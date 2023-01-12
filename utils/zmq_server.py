import zmq
from .settings import LOCAL_IP

status = False
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind('tcp://'+LOCAL_IP)


def run():
    global status
    while True:
        message = socket.recv()
        #print("Received request: %s" % message)
        if message.startswith(b"status"):
            socket.send_string(str(status))
        elif message.startswith(b"set"):
            status = message[4:].decode() == "True"
            print("Status set to", status)
            socket.send_string(str(status))


if __name__ == '__main__':
    run()
