RiftChat

# Description

This is just a chat experiment.

A client just connects through TCP giving a username, sends messages and
receives messages.

There is no password, authentication, chat rooms, private messages, etc.

# RiftChat Protocol

The protocol is simple. The first byte is a code which identifies the type of
message. The rest is a payload corresponding to the message.

# Client

Set username

    100 - {"username": "New Username"}

Send message

    101 - {"message": "New Message"}

Fetch messages after timestamp (no including it)

    102 - ref_timestamp

# Server

Results from message fetch

    200 - messages_num - 'msgs'
