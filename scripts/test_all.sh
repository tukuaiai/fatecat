#!/bin/bash
set -e

echo "Running all tests..."

for service in services/*/; do
    if [ -d "$service/tests" ]; then
        name=$(basename "$service")
        echo "Testing $name..."
        cd "$service"
        python -m pytest tests/ -v
        cd - > /dev/null
    fi
done

echo "All tests passed!"
