#!/bin/bash

docker build --platform linux/amd64 -t zaffnet/namudhaj:prodv0.8 .
docker tag zaffnet/namudhaj:prodv0.8 zaffnet/namudhaj:prodv0.8