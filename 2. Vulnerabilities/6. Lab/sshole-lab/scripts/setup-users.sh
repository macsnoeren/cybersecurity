#!/bin/sh
# No longer used -- accounts are now created inline in the Dockerfiles
# (alice with bcrypt via htpasswd, deploy with shadow forced to "*").
# Kept as a reference for what the accounts look like.
#
# alice : borrow account with a real bcrypt ($2y$) hash
#         (password: correcthorsebatterystaple)
# deploy: key-only/locked account, shadow field = "*" (the SSHole target)
echo "setup-users.sh is deprecated; see Dockerfile.vulnerable" >&2
exit 0
