#!/bin/sh
# Directly probe what musl's crypt() returns for various salt/key-length
# combinations. This proves the mechanism: look for rows ending in "-> *".
#
# Run INSIDE the vulnerable container:
#     docker exec sshole-lab-vulnerable sh /opt/probe.sh
#
# Or from the host:
#     scripts/probe.sh [container_name]
set -eu

# If we're running on the host, exec into the container.
if [ -f /etc/alpine-release ] 2>/dev/null; then
  : # We ARE inside an Alpine container; run directly below.
else
  NAME="${1:-sshole-lab-vulnerable}"
  exec docker exec "$NAME" sh /opt/probe.sh
fi

# We're inside the container now.
apk add --no-cache build-base >/dev/null 2>&1 || true

cat > /tmp/probe.c <<'EOF'
#define _GNU_SOURCE
#include <stdio.h>
#include <string.h>
#include <crypt.h>

static void t(int n, const char *salt){
  char key[4096];
  if (n > 4094) n = 4094;
  memset(key, 'A', n); key[n] = 0;
  char *r = crypt(key, salt);
  printf(" %4d A | \"%-28s\" -> %s\n", n, salt, r ? r : "(NULL)");
}

int main(void){
  const char *salts[] = {
    "$6$CvhFSGk3AHl4k36J",        /* valid sha512 salt (borrow) */
    "$6$abc",                      /* short sha512 salt */
    "$2y$05",                      /* TRUNCATED bcrypt (pick_salt mangle) */
    "$2y$05$NiolY0k0NShKjUezZdrZku", /* fuller bcrypt setting */
    "xx",                          /* DES fallback salt */
    "*",                           /* the target field itself */
  };
  for (unsigned i = 0; i < sizeof(salts)/sizeof(*salts); i++){
    int lens[] = {10, 256, 257, 300, 1024};
    for (unsigned j = 0; j < sizeof(lens)/sizeof(*lens); j++) t(lens[j], salts[i]);
    printf("\n");
  }
  return 0;
}
EOF

cc -O0 -o /tmp/probe /tmp/probe.c -lcrypt 2>/dev/null \
  || cc -O0 -o /tmp/probe /tmp/probe.c

echo "=== musl crypt() return values (rows ending in -> *  are the trigger) ==="
/tmp/probe
printf "musl version : "
apk list --installed 2>/dev/null | grep -i '^musl-[0-9]' || echo "(unknown)"
