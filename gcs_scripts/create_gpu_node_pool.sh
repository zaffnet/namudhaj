#!/bin/bash

# For Llama 2 7B, make sure you have at least 2 L4 GPUs.
# And change machine type to  g2-standard-24
# Change num_nodes and min_nodes to 0 to save cost
# Add --spot to save costs
# Change the corresponding text-generation-inference.yaml based on
# the GPU choice, sharding, model used, etc.

# gcloud container node-pools create n1-standard-8 \
#   --cluster llm-cluster \
#   --accelerator type=nvidia-tesla-t4,count=1,gpu-driver-version=latest \
#   --machine-type n1-standard-8 \
#   --ephemeral-storage-local-ssd=count=1 \
#   --enable-autoscaling --enable-image-streaming \
#   --num-nodes=1 --min-nodes=1 --max-nodes=1 \
#   --node-locations $REGION-a,$REGION-c --region $REGION --spot

# gcloud container node-pools create gpu-node-pool-ephemeral-ssd \
#   --cluster llm-cluster \
#   --accelerator type=nvidia-tesla-t4,count=1,gpu-driver-version=latest \
#   --machine-type n1-standard-8 \
#   --disk-size=100GB \
#   --enable-autoscaling --enable-image-streaming \
#   --num-nodes=1 --min-nodes=1 --max-nodes=1 \
#   --node-locations $REGION-a --region $REGION \
#   --ephemeral-storage-local-ssd=count=1

gcloud container node-pools create node-pool \
  --cluster llm-cluster \
  --machine-type n1-standard-4 \
  --disk-size=50GB \
  --enable-autoscaling --enable-image-streaming \
  --num-nodes=1 --min-nodes=0 --max-nodes=2 \
  --node-locations $REGION-a --region $REGION