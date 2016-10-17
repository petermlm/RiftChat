import socket
from select import select
from queue import Queue
from threading import Thread

from config import Config
import message


class ClientNetwork:
    def __init__(self, config, callback):
        self.config = config
        self.callback = callback

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.config["host"], self.config["port"]))

        self.client_recv = ClientRecv(self.socket, self.callback)
        self.client_recv.start()

    def close(self):
        self.client_recv.terminate()
        self.client_recv.join()
        self.socket.close()

    def sendMessage(self, message):
        self.socket.send(message)


class ClientRecv(Thread):
    def __init__(self, socket, callback):
        Thread.__init__(self)
        self.callback = callback
        self.socket = socket
        self.buff = bytes([])
        self.alive = True

    def run(self):
        while True:
            if not self.alive:
                break

            ready = select([self.socket], [], [], 1)
            if ready[0]:
                self.buff += self.socket.recv(1024)

            while True:
                self.buff, obj = message.loads(self.buff)

                if obj is None:
                    break

                self.callback(obj)

    def terminate(self):
        self.alive = False
