#!/bin/bash
set -e

echo "Building all services..."

for service in services/*/; do
    if [ -f "$service/Dockerfile" ]; then
        name=$(basename "$service")
        echo "Building $name..."
        docker build -t "$name:latest" "$service"
    fi
done

echo "Build complete!"
