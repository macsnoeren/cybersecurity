#!/bin/sh
# SSHole defensive self-assessment (CVE-2026-123158).
#
# Inspects whether ALL preconditions for the SSHole bypass are present.
# This is a DETECTION tool -- it performs no attack.
#
# Run it inside a target container:
#     docker exec sshole-lab-vulnerable sh /opt/assess.sh
#     docker exec sshole-lab-secure     sh /opt/assess.sh
set -eu

echo "===== SSHole / CVE-2026-123158 precondition check ====="
echo

vuln=1  # assume vulnerable, clear on first failing condition

# --- 1. libc: musl -----------------------------------------------------------
printf "libc         : "
if ldd /bin/sh 2>&1 | grep -qi musl; then
  echo "musl detected (no PAM possible) -- precondition MET"
else
  echo "NOT musl -- SSHole precondition not met"
  vuln=0
fi

# --- 2. sshd build: packaged (patched) or from source (unpatched)? -----------
printf "sshd build   : "
ssh -V 2>&1
if apk info -e openssh-server >/dev/null 2>&1; then
  pkg="$(apk info -v 2>/dev/null | grep '^openssh-' | head -1)"
  echo "               apk package present -> ${pkg}"
  echo "               (if -r3 or later: PATCHED by Alpine)"
  vuln=0
else
  echo "               built from upstream tarball, no apk patch -> UNPATCHED"
fi

# --- 3. PAM ------------------------------------------------------------------
printf "PAM          : "
pam_line="$(sshd -T 2>/dev/null | grep -i '^usepam' || true)"
if [ -n "${pam_line}" ]; then
  echo "${pam_line}"
  case "${pam_line}" in
    *yes*) echo "               PAM enabled -- bypass BLOCKED"; vuln=0 ;;
  esac
else
  echo "no PAM (built --without-pam) -> EXPOSED"
fi

# --- 4. PasswordAuthentication ------------------------------------------------
printf "passwordauth : "
pa_line="$(sshd -T 2>/dev/null | grep -i '^passwordauthentication' || true)"
echo "${pa_line:-not set (defaults to yes)}"
case "${pa_line}" in
  *no*) echo "               password auth disabled -- bypass BLOCKED"; vuln=0 ;;
esac

# --- 5. target account with "*" password field --------------------------------
star="$(awk -F: '$2=="*"{print $1}' /etc/shadow 2>/dev/null | tr '\n' ' ' || true)"
printf "'*' targets  : "
if [ -n "${star}" ]; then
  echo "${star}"
else
  echo "(none) -- no bypass target"
  vuln=0
fi

# --- 6. borrow account with real hash -----------------------------------------
borrow="$(awk -F: '$2 ~ /^\$/{print $1}' /etc/shadow 2>/dev/null | tr '\n' ' ' || true)"
printf "borrow accts : "
if [ -n "${borrow}" ]; then
  echo "${borrow}"
else
  echo "(none) -- salt borrow condition not met"
  vuln=0
fi

echo
echo "======================================================"
if [ "${vuln}" -eq 1 ]; then
  echo ">>> VULNERABLE: all preconditions for CVE-2026-123158 are met."
  echo ">>> Mitigate: patch sshd (>= 10.6p2 / distro patch) and/or set"
  echo ">>>           'PasswordAuthentication no'. Re-run this check."
  exit 2
else
  echo ">>> NOT VULNERABLE: at least one precondition is absent."
  exit 0
fi
