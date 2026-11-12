#!/bin/sh
# Stop and remove the SSHole lab containers and network.
# Usage: ./stop.sh
set -eu

cd "$(dirname "$0")"

echo "=== SSHole Lab — stopping ==="
docker compose down
echo "Done. Images are kept for faster restarts."
