#!/bin/bash
CONCURRENT=${1:-1000}
DURATION=${2:-60s}

echo "🧪 TABEEBY Load Test"
echo "Concurrent: $CONCURRENT"
echo "Duration: $DURATION"

# Using hey or ab if available
if command -v hey &> /dev/null; then
    hey -z $DURATION -c $CONCURRENT http://localhost:8000/health
elif command -v ab &> /dev/null; then
    ab -n $((CONCURRENT * 10)) -c $CONCURRENT http://localhost:8000/health
else
    echo "Installing hey..."
    go install github.com/rakyll/hey@latest
    hey -z $DURATION -c $CONCURRENT http://localhost:8000/health
fi
