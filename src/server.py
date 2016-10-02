#!/usr/bin/env python3


import socket
from select import select

import config
import message
from chat_message import ChatMessage
from client_info import ClientInfo


class Server:
    def __init__(self):
        self.client_info = {}

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.socket.bind((config.ip, config.port))
        self.socket.listen(1)

    def main(self):
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
        buff = sock.recv(1024)

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

    def sendAllConnect(self):
        pass

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
    server = Server()
    server.main()
