#!/bin/bash

mkdir -p confs
cp ../src/confs/rift_server.conf confs/rift_server.conf
cp ../src/confs/rift_client.conf confs/rift_client.conf

sudo docker build -t rift-chat-server -f Dockerfile.server ..
sudo docker build -t rift-chat-client -f Dockerfile.client ..
