#!/bin/bash

export IMAGE_NAME=docker.io/zaffnet/namudhaj:prod-0.134
docker build --platform linux/amd64 -t $IMAGE_NAME .
docker tag $IMAGE_NAME $IMAGE_NAME
docker push $IMAGE_NAME
envsubst < configs/gradio-classify.yaml  | kubectl apply -f -