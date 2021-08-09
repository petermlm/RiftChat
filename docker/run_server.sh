#!/bin/bash

docker run \
    -it \
    --rm \
    --name rift-chat-server \
    -p8010:8010 \
    rift-chat-server
