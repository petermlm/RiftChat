#!/usr/bin/env python3


import sys
import socket
import signal
from select import select

from daemon import Daemon
from config import Config
from chat_message import ChatMessage
from client_info import ClientInfo
import message
import log


pid_file = "/tmp/rift_server.pid"


class Server(Daemon):
    def __init__(self, pid_file, config, stdout=None, stderr=None):
        super().__init__(pidfile=pid_file, stdout=stdout, stderr=stderr)

        self.config = config
        self.client_info = {}

    def run(self):
        def handler(_a, _b):
            pass
        signal.signal(signal.SIGTERM, handler)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.socket.bind(("0.0.0.0", self.config["port"]))
        self.socket.listen(1)

        normal_shutdown = False

        while True:
            # Wait for connections
            sockets = [self.socket] + list(self.client_info.keys())

            try:
                (infd, _, _) = select(sockets, [], [])
            except (KeyboardInterrupt, InterruptedError):
                self.sendAllServeDown()
                normal_shutdown = True
                break

            for sock in infd:
                if sock in self.client_info:
                    self.messageFromClient(sock)

                else:
                    self.newConnection(sock)

        if normal_shutdown:
            log.stdout("Shutting down.")

    def messageFromClient(self, sock):
        try:
            buff = sock.recv(1024)
        except ConnectionResetError:
            # A client connection fell
            buff = bytes([])

        if len(buff) == 0:
            log.stdout("Disconnection of %s" % (sock))
            self.sendAllDisconnect(self.client_info[sock].username)
            del self.client_info[sock]
            return

        self.parseClientMessage(sock, buff)

    def newConnection(self, sock):
        conn, addr = sock.accept()
        log.stdout("New connection from %s" % (conn))
        self.client_info[conn] = ClientInfo(conn)

        conn.send(message.dumps({"code": 202, "new": self.client_info[conn].username}))
        self.sendAllConnect(self.client_info[conn].username)

    def parseClientMessage(self, sock, buff):
        self.client_info[sock].buff += buff

        new_buff, obj = message.loads(self.client_info[sock].buff)

        if obj is None:
            return

        if obj["code"] == 100:
            chat_msg = ChatMessage(self.client_info[sock].username, obj["message"])
            self.sendAllMessage(chat_msg)

        elif obj["code"] == 101:
            old_username = self.client_info[sock].username
            self.client_info[sock].username = obj["username"]
            sock.send(message.dumps({"code": 202, "new": obj["username"]}))
            self.usernameChanged(old_username, self.client_info[sock].username)

        self.client_info[sock].buff = new_buff

    def sendAllMessage(self, chat_msg):
        self.sendAll({"code": 200, "message": chat_msg.getObj()})

    def sendAllConnect(self, new):
        self.sendAll({"code": 201, "new": new})

    def usernameChanged(self, old, new):
        self.sendAll({"code": 203, "old": old, "new": new})

    def sendAllDisconnect(self, username):
        self.sendAll({"code": 204, "username": username})

    def sendAllServeDown(self):
        self.sendAll({"code": 205})

    def sendAll(self, obj):
        for client in self.client_info:
            msg = message.dumps(obj)
            self.client_info[client].conn.send(msg)


def printUsage():
    usage_str = \
        "Usage:" \
        "\n" \
        "\tserver.py -d [ start | stop | restart ] {config}\n" \
        "\tserver.py {config}" \
        "\n" \
        "The first way to execute will use riftChat server as a daemon. The" \
        "second optional parametera string for a config file"

    print(usage_str)


if __name__ == "__main__":
    la = len(sys.argv)

    if la < 1 or la > 4:
        printUsage()
        exit(1)

    daemon = False
    daemon_cmd = ""
    config_path = ""

    last_arg_index = 1

    # If flag -d is present, this should be used as a daemon
    if la > last_arg_index and sys.argv[last_arg_index] == "-d":
        daemon = True
        daemon_cmd = sys.argv[2]
        last_arg_index = 3

    # Get configuration file, if any
    if la > last_arg_index:
        config_path = sys.argv[last_arg_index]
        config = Config.serverConf(config_path)
    else:
        config = Config.serverConf()

    server = Server(pid_file,
                    config,
                    stdout="/tmp/rift_stdout.log",
                    stderr="/tmp/rift_stderr.log")

    # Runs until killed
    if not daemon:
        print("Server running on port %s" % (server.config["port"]))
        server.run()
        exit(0)

    # Performs daemon operation
    else:
        if daemon_cmd == "start":
            server.start()
            sys.exit(0)

        elif daemon_cmd == "stop":
            server.stop()
            sys.exit(0)

        elif daemon_cmd == "restart":
            server.restart()
            sys.exit(0)

        print("Unknown daemon command")
        printUsage()
        sys.exit(1)
