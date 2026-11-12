#!/bin/sh
# Build and start the SSHole lab (vulnerable + secure targets).
# Usage: ./start.sh
set -eu

cd "$(dirname "$0")"

echo "=== SSHole Lab — building and starting ==="
echo
docker compose up --build -d
echo
echo "Targets running:"
echo "  vulnerable : ssh deploy@127.0.0.1 -p 2222"
echo "  secure     : ssh deploy@127.0.0.1 -p 2223"
echo
echo "Quick checks:"
echo "  docker exec sshole-lab-vulnerable sh /opt/assess.sh"
echo "  docker exec sshole-lab-vulnerable sh /opt/probe.sh"
echo "  ./scripts/test-bypass.sh 2222 deploy"
