#!/bin/bash
set -e

echo "Building all modules..."

for module in modules/*/; do
    if [ -f "$module/Dockerfile" ]; then
        name=$(basename "$module")
        echo "Building $name..."
        docker build -t "$name:latest" "$module"
    fi
done

echo "Build complete!"
