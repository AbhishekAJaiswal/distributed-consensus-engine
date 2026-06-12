#!/bin/bash

echo "================================"
echo "Chaos Testing Started"
echo "================================"

echo ""
echo "1. Simulating Node Failure..."

docker stop node3

sleep 5

echo ""
echo "2. Restoring Node..."

docker start node3

sleep 5

echo ""
echo "Chaos Test Completed"