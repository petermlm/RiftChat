#!/bin/bash


if [ $# -eq 1 ]
then
    conf_file=$1
else
    conf_file=../src/confs/rift_server.conf
fi

mkdir -p confs
cp $conf_file confs/rift_server.conf

docker build -t rift-chat-server -f Dockerfile.server ..
