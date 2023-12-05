#!/bin/bash

gcloud config set project ece1779project
export PROJECT_ID=$(gcloud config get project)
export REGION=us-central1