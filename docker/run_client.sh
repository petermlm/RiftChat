#!/bin/bash

sudo docker run -it --rm --name rift-chat-client-$1 --net="host" rift-chat-client
