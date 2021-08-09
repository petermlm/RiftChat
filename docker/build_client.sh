#!/bin/bash


if [ $# -eq 1 ]
then
    conf_file=$1
else
    conf_file=../src/confs/rift_client.conf
fi

mkdir -p confs
cp $conf_file confs/rift_client.conf

docker build -t rift-chat-client -f Dockerfile.client ..
