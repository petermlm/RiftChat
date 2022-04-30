# RiftChat

A simple chat made to experiment with basic networking in Python.

# How To Run

## With Docker

There are two containers, for the server and for the client. Simply build them:

    docker-compose build

Containers can be started now. For the server simply do `up`, for clients,
`run` should be used:

    docker-compose up server
    docker-compose run --rm client

Several clients can be started.

## Without docker

For the server, only Python 3 is needed. For the client, urwid is needed, as
specified in the requirements.client.txt file. It is recommended that a virtual
environment is create for it.

Usage of server is:

    python src/server.py
    python src/server.py -d [ start | stop | restart ]

The first way will simply start the server, the second way to execute will use
riftChat server as a daemon.

Client is just

    python src/client.py

# RiftChat Protocol

The protocol is simple. Every message is json. The json always has a code.
Depending on that code, it may have other arguments.

## From Client to Server

### Send message - 100

Client sends a new message to the server. Every connected user will receive
this message.

    {"code": 100, "message": "New Message"}

### Set username - 101

Client changes it's username.

    {"code": 101, "username": "New Username"}

## From Server to Client

### Send message - 200

New message to be displayed. Sent to all users including the original author of
the message.

    {"code": 200, "message": chat_msg.getObj()}

### User connected - 201

State to everyone that a user as connected.

    {"code": 201, "new": "New username"}

### Give new username - 202

Give out new username to specific user. Maybe on connection or on username name
change.

    {"code": 202, "new": "New username"}

### Changed username - 203

State to everyone that a user as changed it's username.

    {"code": 203, "old": "Old username", "new": "New username"}

### User disconnected - 204

State to everyone that a user as disconnected.

    {"code": 204, "username": "Disconnected username"}

### Server went down - 205

State to everyone that the server went down

    {"code": 205}
