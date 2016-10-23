#!/usr/bin/env python3

import sys
import socket
import select
import time
import json
from datetime import datetime

from config import Config
import message
from client_interface import ClientInterface
from client_network import ClientNetwork


class Client:
    def __init__(self, config):
        self.config = config
        self.messages = []
        self.buff = bytes([])

        self.network = ClientNetwork(config, self.handleRecv)
        self.interface = ClientInterface(self.handleInput)

    def handleInput(self, input_str):
        # No input
        if len(input_str) == 0:
            return

        # If this is not a command, then it is a regular message
        if input_str[0] != ":":
            msg = message.dumps({"code": 100, "message": input_str})
            self.network.sendMessage(msg)
            return

        # Else, this is a command, so handle it. Unless if is empty
        if len(input_str) == 1:
            return

        cmd_args = input_str[1:].split()
        cmd = cmd_args[0]
        args = cmd_args[1:]

        if cmd in ["quit", "q"]:
            self.close()
            return

        elif cmd in ["username", "un", "me"]:
            if len(args) != 1:
                self.interface.addLine("Usage :{username|un|me} new_username")
                return
            msg = message.dumps({"code": 101, "username": args[0]})
            self.network.sendMessage(msg)
            return

        else:
            self.interface.addLine("Unknown Command")

    def handleRecv(self, obj):
        if obj["code"] == 200:
            msg = obj["message"]

            dt = datetime.fromtimestamp(
                int(msg["timestamp"] / 1000)
            ).strftime('%Y-%m-%d %H:%M:%S')

            msg_str = "%s|%s|%s" % (
                dt,
                msg["username"],
                msg["message"])

            self.interface.addLine(msg_str)

        elif obj["code"] == 201:
            self.interface.addLine("Username %s connected" % (obj["new"]))

        elif obj["code"] == 202:
            self.interface.addLine("Your new username is: %s" % (obj["new"]))

        elif obj["code"] == 203:
            msg_str = "User %s changed name to %s" % (
                obj["old"], obj["new"])
            self.interface.addLine(msg_str)

        elif obj["code"] == 204:
            msg_str = "User %s disconnected" % (obj["username"])
            self.interface.addLine(msg_str)

        elif obj["code"] == 205:
            self.interface.addLine("!!! Server is Down !!!")
            self.interface.addLine("Shutting down in 3 seconds")
            time.sleep(3)
            self.close()

    def close(self):
        self.interface.addLine("Disconnecting...")
        self.network.close()
        self.interface.addLine("Shutting down...")
        self.interface.exit()

    def main(self):
        self.network.connect()
        self.interface.startInterface()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        config = Config.clientConf(sys.argv[1])
    else:
        config = Config.clientConf()

    Client(config).main()
