import utils.zmq_server
import utils.tcp_server
import utils.telegram_bot

import threading
if __name__ == '__main__':
    thread1 = threading.Thread(target=utils.zmq_server.run)
    thread2 = threading.Thread(target=utils.tcp_server.run)
    thread1.start()
    thread2.start()
    utils.telegram_bot.run()