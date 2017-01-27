RiftChat

# Versions

v0.3.1

# Description

A simple chat made to text basic networking in Python.

# How To Run

## With Docker

Go into the docker directory and execute the `build.sh` script. This is build
two images, one for the server and another for the client.

Then run the server with `run_server.sh` and a client with `run_client.sh`. The
client script receives an argument that is appended to the name of the
container. So running:

    ./run_client.sh c1

will make a container with the name:

    rift-chat-client-c1

## Without docker

You will need Python3 for both client and server. For the client you will also
need urwid as specified in the requirements.txt file.

Usage of server is:

    server.py -d [ start | stop | restart ] {config}\n
    server.py {config}

The first way to execute will use riftChat server as a daemon. The second
optional parameter string for a config file.

Client is just

    client.py {config}

Where config may be a path for a config file.

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
