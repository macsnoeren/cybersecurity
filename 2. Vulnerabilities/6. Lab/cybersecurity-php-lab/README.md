# cybersecurity-php-lab

A **local, isolated security-research lab**: a Docker image running PHP under
**Apache `mod_php`**, serving a simple PHP page, used to study PHP
vulnerabilities — chiefly **PHP2Shell** (CVE-2026-109618 / CVE-2026-109619) —
the same purpose as [vulhub](https://github.com/vulhub/vulhub) or
[DVWA](https://github.com/digininja/DVWA). The PHP version is a build arg; via
Compose it defaults to the **pre-fix** `8.3.35-apache` (vulnerable), and you can
opt into a patched build (see below).

> ⚠️ **A pre-fix build is intentionally insecure.**
> The default Compose build carries known, actively-exploited RCE.
> The Compose file publishes the port on `127.0.0.1` only. Keep it that way.
> Never run this on a machine reachable from an untrusted network, and never
> put real data in it.

> **Standalone by design.** This lab is intentionally **not** wired into any
> deployment node (no `DOCKER_BUILD_IMAGES` entry, no node `compose.yml`
> service). It is built and run only on demand with the `docker compose`
> commands below, and must stay separate from the deployment.

## What's in here

| File | Purpose |
|------|---------|
| `Dockerfile` | `php:${PHP_VERSION}-apache` (default `8.3-apache`) — Apache httpd with `mod_php` (the `apache2handler` SAPI) already wired in. |
| `docker-compose.yml` | Builds and runs the lab (`PHP_VERSION` default `8.3.35-apache`, pre-fix), bound to `127.0.0.1:8080`, on its own bridge network. |
| `www/index.php` | The simple PHP page: reports the running PHP version / SAPI / server and warns when the build is in the PHP2Shell range. |
| `www/php2shell.php` | Defensive self-assessment for CVE-2026-109618 / -109619 (version + mitigation check). No exploit. |
| `www/info.php` | `phpinfo()` — confirms the exact build and that `mod_php` is active. |

## Run it

From the top of this repository (or from this directory — both work):

```sh
cd projects/cybersecurity-php-lab
docker compose up --build
```

Then open <http://127.0.0.1:8080/>. You should see the lab page reporting the
running PHP version and SAPI `apache2handler` (that's `mod_php`). The PHP2Shell
assessment is at <http://127.0.0.1:8080/php2shell.php> and `phpinfo()` is at
<http://127.0.0.1:8080/info.php>.

Stop and remove it with:

```sh
docker compose down
```

## PHP2Shell — CVE-2026-109618 & CVE-2026-109619

**PHP2Shell** is the pair of PHP vulnerabilities disclosed **2026-10-21**:

| | |
|---|---|
| CVE-2026-109618 | RCE via out-of-memory corruption during request cleanup (one vector is `session.upload_progress`). |
| CVE-2026-109619 | RCE via stale request-owned global state reused by a later request on the same worker (multipart parser). |
| Severity | **CVSS v4.0 9.2**, **unauthenticated remote code execution**. |
| Who is affected | **All PHP installations serving web requests** — this is *not* an "old version only" or CGI-only bug; `mod_php` is affected too. |
| Fixed in | **8.2.35 · 8.3.36 · 8.4.27 · 8.5.12** (minimal source backports exist for 7.4 / 8.0 / 8.1; older branches are EOL). |
| Status | Being **exploited in the wild**; treat patching as urgent on real systems. |

So the target just has to be *unpatched* — not old. Via Compose this lab
defaults to the **pre-fix** `8.3.35-apache`, a deliberate study target. Pick a
different pin, or a patched build to compare against, with `PHP_VERSION`:

```sh
PHP_VERSION=8.4.26-apache docker compose up -d --build   # other pre-fix branch
PHP_VERSION=8.3-apache    docker compose up -d --build   # patched (safe)
```

Visit **`/php2shell.php`** either way — it reports whether the running build is
in the vulnerable range, checks the mitigation settings, and gives remediation.

### What this lab does and does not contain

This lab ships the **vulnerable target runtime** (when you opt into a pre-fix
pin) and a **defensive assessment page**. It does **not** contain a working
exploit or proof-of-concept for CVE-2026-109618 / -109619, and I won't add one:
a weaponized chain for a freshly-disclosed, actively-exploited, unauthenticated
RCE that affects essentially every unpatched PHP server is real-world attack
capability, and the teachable part of a classroom demo — the vulnerable target,
the root cause, detection, and remediation — doesn't require it.

For the mechanism and defensive detail, use the authoritative write-ups:

- PHP's official advisories: **GHSA-w8hw-w9fx-j79w** and **GHSA-6wmf-4rv5-p3rp**
- [watchTowr — CVE-2026-109618 FAQ](https://watchtowr.com/intelligence/php-cve-2026-109618-faq/)
- [Datadog Security Labs — PHP2Shell analysis](https://securitylabs.datadoghq.com/articles/php2shell-critical-vulnerabilities-in-php/)

If your course needs a hands-on *exploitation* exercise, run it against a
published, consented training target (e.g. a vulhub reproduction) using the
public PoCs referenced in those advisories, inside this kind of isolated lab.

## Wire it into the monorepo (submodule)

Projects in `projects/` are git **submodules**, one per repo (see
`projects/README.md`). This directory is plain local source until you give it a
home repo:

```sh
# 1. create an EMPTY repo on your git host, then from the top of this repo:
cd <top of this repository>
git -C projects/cybersecurity-php-lab init
git -C projects/cybersecurity-php-lab add .
git -C projects/cybersecurity-php-lab commit -m "Initial PHP security lab"
git -C projects/cybersecurity-php-lab remote add origin <url>
git -C projects/cybersecurity-php-lab push -u origin main

# 2. adopt it as a submodule in place
git submodule add -b main <url> projects/cybersecurity-php-lab
git submodule absorbgitdirs
git commit -m "projects: add cybersecurity-php-lab"
```

Until then you can build and run it directly with the `docker compose` commands
above — it does not need to be a submodule to work.
