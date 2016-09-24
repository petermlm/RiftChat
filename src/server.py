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
        self.chat_entries = []

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
            del self.client_info[sock]
            return

        self.parseClientMessage(sock, buff)

    def newConnection(self, sock):
        conn, addr = sock.accept()
        print("New connection from %s" % (conn))
        self.client_info[conn] = ClientInfo(conn)

    def parseClientMessage(self, sock, buff):
        self.client_info[sock].buff += buff

        new_buff, obj = message.loads(self.client_info[sock].buff)

        if obj is None:
            return

        if obj["code"] == 100:
            self.client_info[sock].username = obj["username"]
            sock.send(message.dumps({"code": 200, "Res": "Welcome: %s" % (obj["username"])}))

        elif obj["code"] == 101:
            chat_msg = ChatMessage(self.client_info[sock].username, obj["message"])
            self.chat_entries.append(chat_msg)

        elif obj["code"] == 102:
            msgs = []

            for i in self.chat_entries:
                if i.timestamp <= obj["ref_time"]:
                    continue

                msgs.append(i.getObj())

            sock.send(message.dumps({"code": 201, "messages": msgs}))

        self.client_info[sock].buff = new_buff


if __name__ == "__main__":
    server = Server()
    server.main()
