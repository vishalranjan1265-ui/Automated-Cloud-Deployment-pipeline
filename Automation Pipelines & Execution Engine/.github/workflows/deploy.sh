#!/usr/bin/env bash

set -euo pipefail

AWS_REGION="${AWS_REGION:-us-east-1}"
AWS_ACCOUNT_ID="${AWS_ACCOUNT_ID}"
ECR_REPO_NAME="${ECR_REPO_NAME:-cloud-auto-deploy-app}"

export ECR_IMAGE_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO_NAME}:latest"

echo "==> [1/4] Authenticating runtime build engines with remote ECR cluster..."
aws Ecr get-login-password --region "${AWS_REGION}" | docker login --username AWS --password-stdin "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

echo "==> [2/4] Triggering Docker contextual build configurations from parent boundary..."
docker build -t "${ECR_REPO_NAME}:latest" -f ../Dockerfile ..
docker tag "${ECR_REPO_NAME}:latest" "${ECR_IMAGE_URI}"

echo "==> [3/4] Dispatching application image layer payloads to central registry..."
docker push "${ECR_IMAGE_URI}"

echo "==> [4/4] Activating programmatic provisioning engine execution loops..."
python3 ../deploy.py

echo "==> [COMPLETE] Multi-tiered deployment script executed successfully."