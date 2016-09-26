#!/usr/bin/env python3

import sys
import socket
import select
import time
import json

import config
import message
from client_interface import ClientInterface


class Client:
    def __init__(self):
        self.messages = []
        self.buff = bytes([])

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((config.ip, config.port))

    def close(self):
        self.socket.close()

    def sendMessage(self, message):
        self.socket.send(message)

    def getMessage(self):
        ready = select.select([self.socket], [], [], 1)
        if ready[0]:
            return self.socket.recv(1024)

        return bytes([])

    def main(self):
        self.connect()

        while True:
            input_str = input("$ ").split(" ")

            cmd = input_str[0]

            if cmd.lower() in ["q", "quit"]:
                break

            elif cmd.lower() in ["username", "un", "me"]:
                msg = message.dumps({"code": 100, "username": input_str[1]})
                self.sendMessage(msg)

            elif cmd.lower() in ["send", "s"]:
                msg = message.dumps({"code": 101, "message": " ".join(input_str[1:])})
                self.sendMessage(msg)

            elif cmd.lower() in ["messages", "msgs", "g"]:
                now = int(time.time() * 1000)
                msg = message.dumps({"code": 102, "ref_time": now - 50000})
                self.sendMessage(msg)

            elif cmd.lower() in ["get", "g"]:
                self.buff += self.getMessage()

                self.buff, obj = message.loads(self.buff)

                if obj is not None:
                    print(obj)

            else:
                print("Unknown Command")

        self.close()


if __name__ == "__main__":
    def some(text): pass
    ci = ClientInterface(some)
    ci.startInterface()
    exit(1)

    client = Client()
    client.main()
    exit(1)

    client.connect()

    client.sendMessage(message.dumps({"code": 100, "username": sys.argv[1]}))
    time.sleep(0.5)
    client.sendMessage(message.dumps({"code": 101, "message": "This is a message"}))
    time.sleep(0.5)
    client.sendMessage(message.dumps({"code": 101, "message": "This too, is a message"}))
    time.sleep(0.5)
    client.sendMessage(message.dumps({"code": 102, "ref_time": 0}))

    time.sleep(1)

    print("Getting messages")
    buff, msgs = message.loads(client.getMessage())
    print(msgs)
    buff, msgs = message.loads(buff)
    print(msgs)

    client.close()
