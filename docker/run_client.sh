#!/bin/bash

sudo docker run \
    -it \
    --rm \
    --name rift-chat-client-$1 \
    -v $(pwd)/confs:/tmp/confs \
    --net="host" \
    rift-chat-client
