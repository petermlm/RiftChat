#!/usr/bin/env python3


import sys
import socket
from select import select

from daemon import Daemon
from config import Config
import message
from chat_message import ChatMessage
from client_info import ClientInfo


pid_file = "/tmp/rift_server.pid"


class Server(Daemon):
    def __init__(self, pid_file, config):
        super().__init__(pidfile=pid_file)

        self.config = config
        self.client_info = {}

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.socket.bind((self.config["host"], self.config["port"]))
        self.socket.listen(1)

        normal_shutdown = False

        while True:
            # Wait for connections
            sockets = [self.socket] + list(self.client_info.keys())

            try:
                (infd, _, _) = select(sockets, [], [])
            except KeyboardInterrupt:
                normal_shutdown = True
                break

            for sock in infd:
                if sock in self.client_info:
                    self.messageFromClient(sock)

                else:
                    self.newConnection(sock)

        if normal_shutdown:
            print("Shutting down.")

    def messageFromClient(self, sock):
        try:
            buff = sock.recv(1024)
        except ConnectionResetError:
            # A client connection fell
            buff = bytes([])

        if len(buff) == 0:
            print("Disconnection of %s" % (sock))
            self.sendAllDisconnect(self.client_info[sock].username)
            del self.client_info[sock]
            return

        self.parseClientMessage(sock, buff)

    def newConnection(self, sock):
        conn, addr = sock.accept()
        print("New connection from %s" % (conn))
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

    def sendAll(self, obj):
        for client in self.client_info:
            msg = message.dumps(obj)
            self.client_info[client].conn.send(msg)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        config = Config.serverConf(sys.argv[2])
    else:
        config = Config.serverConf()

    server = Server(pid_file, config)

    if len(sys.argv) >= 2:
        if 'start' == sys.argv[1]:
            server.start()
            sys.exit(0)

        elif 'stop' == sys.argv[1]:
            server.stop()
            sys.exit(0)

        elif 'restart' == sys.argv[1]:
            server.restart()
            sys.exit(0)

        else:
            print("Unknown command")
            sys.exit(1)

    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(1)
