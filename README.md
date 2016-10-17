RiftChat

# Versions

v0.0 - First working prototype implementation

# Description

TODO

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
