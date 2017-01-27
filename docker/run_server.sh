#!/bin/bash

sudo docker run \
    -dit \
    --name rift-chat-server \
    -v confs:/tmp/confs \
    -p8000:8000 rift-chat-server
