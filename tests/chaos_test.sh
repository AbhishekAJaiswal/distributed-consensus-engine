#!/bin/bash
set -euo pipefail

PROJECT_NAME="distributed-consensus-engine"

function abort() {
  echo "ERROR: $1" >&2
  exit 1
}

function ensure_container_exists() {
  local container="$1"
  if ! docker inspect "$container" >/dev/null 2>&1; then
    abort "Container '$container' not found. Ensure the compose stack is up and the container name matches."
  fi
}

function wait_for_container_state() {
  local container="$1"
  local desired_state="$2"
  local timeout=30
  local elapsed=0
  local state

  while [ "$elapsed" -lt "$timeout" ]; do
    state=$(docker inspect -f '{{.State.Status}}' "$container")
    if [ "$state" = "$desired_state" ]; then
      return 0
    fi
    sleep 1
    elapsed=$((elapsed + 1))
  done

  abort "Timeout waiting for '$container' to become '$desired_state'. Current state: $state"
}

function wait_for_network_disconnection() {
  local container="$1"
  local network="$2"
  local timeout=30
  local elapsed=0

  while [ "$elapsed" -lt "$timeout" ]; do
    if ! docker network inspect "$network" >/dev/null 2>&1; then
      abort "Network '$network' does not exist."
    fi
    if ! docker network inspect "$network" -f '{{range .Containers}}{{.Name}}{{"\n"}}{{end}}' | grep -q "^${container}$"; then
      return 0
    fi
    sleep 1
    elapsed=$((elapsed + 1))
  done

  abort "Timeout waiting for '$container' to disconnect from network '$network'."
}

function wait_for_network_connection() {
  local container="$1"
  local network="$2"
  local timeout=30
  local elapsed=0

  while [ "$elapsed" -lt "$timeout" ]; do
    if ! docker network inspect "$network" >/dev/null 2>&1; then
      abort "Network '$network' does not exist."
    fi
    if docker network inspect "$network" -f '{{range .Containers}}{{.Name}}{{"\n"}}{{end}}' | grep -q "^${container}$"; then
      return 0
    fi
    sleep 1
    elapsed=$((elapsed + 1))
  done

  abort "Timeout waiting for '$container' to connect to network '$network'."
}

function find_compose_network() {
  local project_name="$1"
  docker network ls --filter "name=${project_name}_default" --format '{{.Name}}' | head -n 1
}

NETWORK_NAME=$(find_compose_network "$PROJECT_NAME")
if [ -z "$NETWORK_NAME" ]; then
  NETWORK_NAME="${PROJECT_NAME}_default"
fi

echo "=================================="
echo " CHAOS TEST STARTED"
echo "=================================="

echo ""
echo "1. Simulating Node Failure..."
ensure_container_exists node3
docker stop node3

sleep 10

echo ""
echo "2. Restoring Node..."
docker start node3
wait_for_container_state node3 "running"

sleep 5

echo ""
echo "3. Simulating Network Partition..."
ensure_container_exists node4
docker network disconnect "$NETWORK_NAME" node4
wait_for_network_disconnection node4 "$NETWORK_NAME"

sleep 10

echo ""
echo "4. Reconnecting Node4..."
docker network connect "$NETWORK_NAME" node4
wait_for_network_connection node4 "$NETWORK_NAME"

sleep 5

echo ""
echo "5. Verifying Cluster Status..."
docker ps --filter "name=node"

echo ""
echo "=================================="
echo " CHAOS TEST COMPLETED"
echo "=================================="