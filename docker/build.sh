#!/bin/bash

sudo docker build -t rift-chat-server -f Dockerfile.server ..
sudo docker build -t rift-chat-client -f Dockerfile.client ..
