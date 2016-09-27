#!/usr/bin/env python3

import sys
import socket
import select
import time
import json
from datetime import datetime

import config
import message
from client_interface import ClientInterface
from client_network import ClientNetwork


class Client:
    def __init__(self):
        self.messages = []
        self.buff = bytes([])

        self.network = ClientNetwork(self.handleRecv)
        self.interface = ClientInterface(self.handleInput)

    def handleInput(self, input_str):
        cmd_args = input_str.split()
        cmd = cmd_args[0]
        args = cmd_args[1:]

        if cmd.lower() in ["q", "quit"]:
            return

        elif cmd.lower() in ["username", "un", "me"]:
            msg = message.dumps({"code": 100, "username": args[0]})
            self.network.sendMessage(msg)

        elif cmd.lower() in ["send", "s"]:
            msg = message.dumps({"code": 101, "message": " ".join(args[0:])})
            self.network.sendMessage(msg)

        elif cmd.lower() in ["messages", "msgs", "g"]:
            now = int(time.time() * 1000)
            msg = message.dumps({"code": 102, "ref_time": now - 50000})
            self.network.sendMessage(msg)

        # elif cmd.lower() in ["get", "g"]:
        #     self.buff += self.network.getMessage()
        #
        #     self.buff, obj = message.loads(self.buff)
        #
        #     if obj is not None:
        #         self.interface.addLine(str(obj))

        else:
            self.interface.addLine("Unknown Command")

    def handleRecv(self, obj):
        self.interface.addLine("In here")
        if obj["code"] == 200:
            self.interface.addLine("200")
            self.interface.addLine(obj["Res"])

        elif obj["code"] == 201:
            self.interface.addLine("201")
            for msg in obj["messages"]:
                dt = datetime.fromtimestamp(
                    int(msg["timestamp"] / 1000)
                ).strftime('%Y-%m-%d %H:%M:%S')

                msg_str = "%s|%s|%s" % (
                    dt,
                    msg["username"],
                    msg["message"])

                self.interface.addLine(msg_str)


    def main(self):
        self.network.connect()
        self.interface.startInterface()
        self.network.close()


if __name__ == "__main__":
    client = Client()
    client.main()
    exit(1)

    def cb(obj): print(obj)
    client = ClientNetwork(cb)
    client.connect()

    client.sendMessage(message.dumps({"code": 100, "username": sys.argv[1]}))
    time.sleep(0.5)
    client.sendMessage(message.dumps({"code": 101, "message": "This is a message"}))
    time.sleep(0.5)
    client.sendMessage(message.dumps({"code": 101, "message": "This too, is a message"}))
    time.sleep(0.5)
    client.sendMessage(message.dumps({"code": 102, "ref_time": 0}))

    client.sendMessage(message.dumps({"code": 101, "message": "Ai"}))
    client.sendMessage(message.dumps({"code": 101, "message": "Ui"}))
    client.sendMessage(message.dumps({"code": 101, "message": "Ei"}))
    client.sendMessage(message.dumps({"code": 102, "ref_time": 0}))

    time.sleep(4)

    client.close()
