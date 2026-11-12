#!/bin/sh
# Start sshd in the foreground with logging to stderr so `docker logs` shows
# authentication events (used in the detection exercise).
set -eu

# Regenerate host keys if they are missing (e.g. keys were not baked in).
[ -f /etc/ssh/ssh_host_ed25519_key ] || ssh-keygen -A

exec /usr/sbin/sshd -D -e
