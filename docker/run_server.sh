#!/bin/bash

sudo docker run \
    -dit \
    --rm \
    --name rift-chat-server \
    -v $(pwd)/confs:/tmp/confs \
    -p8000:8000 \
    rift-chat-server
