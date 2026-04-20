#!/bin/bash
set -e

echo "Running all tests..."

for module in modules/*/; do
    if [ -d "$module/tests" ]; then
        name=$(basename "$module")
        echo "Testing $name..."
        cd "$module"
        python -m pytest tests/ -v
        cd - > /dev/null
    fi
done

echo "All tests passed!"
