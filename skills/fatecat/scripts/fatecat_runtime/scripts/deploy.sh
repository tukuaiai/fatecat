#!/bin/bash
set -e

echo "Deploying modules..."

# Build images
./scripts/build_all.sh

# Apply Kubernetes configs
kubectl apply -f infrastructure/kubernetes/

echo "Deployment complete!"
