RiftChat

# Versions

v0.0 - First working prototype implementation

# Description

This is just a chat experiment.

A client just connects through TCP giving a username, sends messages and
receives messages.

There is no password, authentication, chat rooms, private messages, etc.

# RiftChat Protocol

The protocol is simple. Every message is made up of one byte plus a payload.
The first byte states the size of the payload. The payload is just a json file.

Each json file contains at least a field called code. The rest of the json is
according to the following:

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

### Set username - 201

State to the user that asked for a username change that is was done.

    {"code": 201, "Res": "Some text"}

### Changed username - 202

State to everyone that a user as changed it's username.

    {"code": 202, "old": "Old username", "new": "New username"}

### User disconnected - 203

State to everyone that a user as disconnected.

    {"code": 203, "username": "Disconnected username"}
