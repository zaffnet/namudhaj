#!/bin/bash

kubectl create secret generic llm-cluster \
    --from-literal=OPENAI_API_KEY=${OPENAI_API_KEY} \
    --from-literal=OPENAI_ORG_ID=${OPENAI_ORG_ID} \
    --dry-run=client -o yaml > config/openai-secret.yaml