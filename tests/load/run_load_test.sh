#!/bin/bash

# Default values
USERS=100
SPAWN_RATE=10
RUNTIME=5m
HOST="http://localhost:8888"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --users)
            USERS="$2"
            shift 2
            ;;
        --spawn-rate)
            SPAWN_RATE="$2"
            shift 2
            ;;
        --runtime)
            RUNTIME="$2"
            shift 2
            ;;
        --host)
            HOST="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "Starting load test with:"
echo "Users: $USERS"
echo "Spawn rate: $SPAWN_RATE users/second"
echo "Runtime: $RUNTIME"
echo "Host: $HOST"

# Run locust
locust \
    --host "$HOST" \
    --users "$USERS" \
    --spawn-rate "$SPAWN_RATE" \
    --run-time "$RUNTIME" \
    --headless \
    --only-summary \
    --locustfile locustfile.py 