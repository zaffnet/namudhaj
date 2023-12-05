#!/bin/bash

kubectl create secret generic llm-cluster \
    --from-literal=HUGGING_FACE_TOKEN=${HF_TOKEN} \
    --dry-run=client -o yaml > hf-secret.yaml
