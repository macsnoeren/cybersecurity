# SSHole – OpenSSH Authentication Bypass

**CVE:** CVE-2026-123158  
**Naam:** SSHole  
**Publicatiedatum:** 5 november 2026  
**Getroffen componenten:** OpenSSH en musl libc  
**Opgelost in:** OpenSSH 10.6p2 (of distributiepatches)

> ⚠️ **De kwetsbare container is bewust onveilig.** Deze lab-map bevat een
> opzettelijk kwetsbaar Alpine/OpenSSH-doel. `docker-compose.yml` publiceert de
> poorten uitsluitend op `127.0.0.1`. Houd dat zo. Draai dit nooit op een
> machine die vanaf een onvertrouwd netwerk bereikbaar is, en zet er geen echte
> data op.

> **Op zichzelf staand.** Net als `cybersecurity-php-lab` is deze lab bewust
> **niet** gekoppeld aan een deployment-node. Hij wordt alleen op aanvraag
> gebouwd en gedraaid met de `docker compose`-commando's hieronder.

### Inhoud van deze map

| Bestand | Doel |
|---------|------|
| `Dockerfile.vulnerable` | **Kwetsbaar** Alpine-doel: compileert **upstream OpenSSH 9.6p1 van source** (`--without-pam`) zodat de unpatched crypt()-vergelijking aanwezig is. Alpine's eigen openssh-pakket is al gepatcht. |
| `Dockerfile.secure` | **Niet-kwetsbaar** Alpine-doel: gebruikt Alpine's gepatchte openssh-pakket + `PasswordAuthentication no`. |
| `docker-compose.yml` | Bouwt en draait beide doelen, gebonden aan `127.0.0.1:2222` (kwetsbaar) en `127.0.0.1:2223` (veilig). |
| `config/sshd_config.vulnerable` | sshd-config met de kwetsbare instellingen (`PasswordAuthentication yes`). |
| `config/sshd_config.secure` | Geharde sshd-config (wachtwoordauthenticatie uit). |
| `scripts/assess.sh` | **Defensief**: controleert of een doel aan alle SSHole-precondities voldoet. Geen aanval. |
| `scripts/probe.sh` | **Diagnostisch**: roept musl's `crypt()` direct aan met diverse salts/lengtes. Bewijst het mechanisme — zoek rijen die eindigen op `-> *`. |
| `scripts/test-bypass.sh` | Demonstratie/test tegen het **eigen** loopback-doel. Gebruikt `expect` of `SSH_ASKPASS`. |
| `entrypoint.sh` | Genereert hostkeys en start `sshd` op de voorgrond met logging. |

## 1. Wat is SSHole?

SSHole is een kwetsbaarheid in OpenSSH waardoor een aanvaller onder specifieke omstandigheden SSH-authenticatie kan omzeilen zonder het juiste wachtwoord te kennen.

De kwetsbaarheid ontstaat door een combinatie van OpenSSH, musl libc en een configuratie waarbij PAM niet wordt gebruikt.

De kwetsbaarheid is vooral relevant voor Alpine Linux en andere Linux-systemen die musl gebruiken.

## 2. Technische oorzaak

De kwetsbaarheid ontstaat door een foutieve interpretatie van de foutwaarde van de functie `crypt()`.

In `/etc/shadow` kan een account de waarde `*` hebben als wachtwoordveld. Dit betekent dat het account geen bruikbare wachtwoordhash heeft.

Bij een wachtwoordcontrole gebeurt het volgende:

1. OpenSSH probeert het aangeboden wachtwoord te hashen met `crypt()`.
2. Bij bepaalde configuraties gebruikt OpenSSH de salt van een ander account.
3. musl libc weigert een wachtwoord dat langer is dan 256 bytes.
4. Bij deze fout retourneert musl de waarde `*`.
5. OpenSSH vergelijkt het resultaat met het opgeslagen wachtwoordveld.
6. Omdat beide waarden `*` zijn, wordt de vergelijking succesvol.

Hierdoor kan authenticatie onterecht slagen.

## 3. Wanneer is een systeem kwetsbaar?

De volgende voorwaarden moeten samen aanwezig zijn:

- Linux gebruikt musl libc.
- OpenSSH is ouder dan 10.6p2 en bevat geen distributiepatch.
- OpenSSH draait zonder PAM.
- `PasswordAuthentication yes` staat ingeschakeld.
- Er bestaat een account met `*` als wachtwoordveld.
- Minimaal één ander lokaal account heeft een `$5$`- of `$6$`-wachtwoordhash.

Alpine Linux is een bekend voorbeeld. Ook OpenWrt, Buildroot en Yocto-systemen kunnen getroffen zijn als ze aan deze voorwaarden voldoen.

Niet iedere Alpine Docker-container is kwetsbaar: er moet daadwerkelijk een kwetsbare SSH-server draaien.

## 4. Exploitatie

Een aanvaller heeft netwerktoegang tot de SSH-server nodig en moet de naam van een geschikt account kennen.

Door een speciaal lang wachtwoord aan te bieden (257 tot 1024 bytes) kan de foutieve hashvergelijking worden geactiveerd.

De aanvaller kan hierdoor zonder geldig wachtwoord toegang krijgen tot het betreffende account.

## 5. Impact

- Ongeautoriseerde SSH-toegang.
- Mogelijke toegang tot accounts die uitsluitend voor SSH-keys bedoeld zijn.
- Mogelijke root-toegang, afhankelijk van de accountconfiguratie en verdere rechten.
- Mogelijkheid tot verdere compromittering van het systeem.

## 6. Detectie en mitigatie

**Oplossing:**
- Upgrade OpenSSH naar 10.6p2 of een door de distributie gepatchte versie.
- Herstart de SSH-service na de upgrade.

**Tijdelijke mitigatie:**
- Schakel wachtwoordauthenticatie uit met `PasswordAuthentication no`.
- Beperk netwerktoegang tot SSH.

**Detectie:**
- Controleer SSH-logs op succesvolle wachtwoordauthenticaties van accounts die geen wachtwoord behoren te hebben.
- Onderzoek verdachte logins, nieuwe accounts en gewijzigde SSH-authorized keys.

## 7. Praktische demonstratie

Voor een ethical-hackingpracticum kan een geïsoleerde Docker-omgeving worden gebruikt:

- **Target:** Alpine Linux met een kwetsbare OpenSSH-configuratie.
- **Attacker:** Kali Linux met een SSH-client.
- **Doel:** de authenticatie-bypass demonstreren.
- **Detectie:** SSH-logs onderzoeken.
- **Mitigatie:** OpenSSH patchen en de aanval opnieuw uitvoeren.

Gebruik uitsluitend een geïsoleerde testomgeving.

## 8. Labomgeving in deze map

Deze map implementeert precies dat practicum met **twee Alpine-containers**:
een kwetsbaar doel en een niet-kwetsbaar doel, zodat je het verschil
voor-en-na kunt meten.

### 8.1 Bouwen en starten

```sh
cd "2. Vulnerabilities/6. Lab/sshole-lab"
docker compose up --build -d
```

Twee SSH-doelen draaien nu op loopback:

| Doel | Poort | Eigenschappen |
|------|-------|---------------|
| `sshole-lab-vulnerable` | `127.0.0.1:2222` | Alpine 3.19 + **upstream OpenSSH 9.6p1 van source** (`--without-pam`), `PasswordAuthentication yes`, account `deploy` met `*`. |
| `sshole-lab-secure` | `127.0.0.1:2223` | Alpine 3.21 + **Alpine's gepatchte openssh-pakket**, `PasswordAuthentication no`. |

Beide containers hebben dezelfde accounts:

- **`alice`** — borrow-account met een bcrypt (`$2y$`) wachtwoordhash
  (wachtwoord `correcthorsebatterystaple`). sshd leent haar salt via
  `pick_salt()`.
- **`deploy`** — key-only/locked account met `*` als wachtwoordveld; dit is
  het doelwit van de SSHole-bypass.

> **Waarom OpenSSH van source?** Alpine's eigen openssh-pakket (zelfs op 3.19)
> bevat al een gebackporte fix (`openssh-9.6_p1-r3`). Om de daadwerkelijke bug
> te reproduceren compileert de kwetsbare image upstream OpenSSH 9.6p1 met
> `--without-pam`. Zo is het unpatched crypt()-vergelijkingpad aanwezig.

### 8.2 Detectie (defensief)

Controleer per container of het SSHole-patroon aanwezig is — dit voert **geen**
aanval uit:

```sh
docker exec sshole-lab-vulnerable sh /opt/assess.sh   # => matcht het patroon
docker exec sshole-lab-secure     sh /opt/assess.sh   # => matcht NIET
```

Het script toetst alle zes precondities uit sectie 3: musl libc, unpatched
sshd-build, geen PAM, `PasswordAuthentication yes`, een `*`-account, en een
borrow-account met een echte hash.

### 8.3 Het mechanisme bewijzen met probe.sh

Voordat je de bypass uitvoert, kun je het crypt()-mechanisme direct observeren:

```sh
docker exec sshole-lab-vulnerable sh /opt/probe.sh
```

Zoek rijen die eindigen op `-> *` — dat is de trigger. Voorbeeld-output:

```
  256 A | "$6$CvhFSGk3AHl4k36J"  -> $6$CvhF...   (echte hash)
  257 A | "$6$CvhFSGk3AHl4k36J"  -> *             (TRIGGER: musl weigert > 256)
   10 A | "$2y$05"                -> *             (afgekapte bcrypt: altijd *)
```

### 8.4 De bypass uitvoeren (geïsoleerde lab)

Vereist: `python3` op de host. Gebruikt `expect` als dat beschikbaar is
(interactieve shell), anders `SSH_ASKPASS` (commando-uitvoer).

```sh
# kwetsbaar doel -> login SLAAGT (300-byte wachtwoord op een '*'-account)
scripts/test-bypass.sh 2222 deploy

# veilig doel -> dezelfde poging wordt GEWEIGERD
scripts/test-bypass.sh 2223 deploy
```

Verwachte output op het kwetsbare doel:

```
[+] LOGIN SUCCEEDED as deploy -- uid=1001
```

Dit is een account met `*` als wachtwoordveld — het hoort helemaal geen
wachtwoord-login te accepteren. Het 300-byte wachtwoord triggert musl's
crypt() om `*` te retourneren, wat matcht met het opgeslagen veld.

### 8.5 Detectie in de logs

De succesvolle (of geweigerde) login verschijnt in de sshd-logs:

```sh
docker logs sshole-lab-vulnerable
```

Kijk naar deze regel:

```
Accepted password for deploy from 172.18.0.1 port XXXXX ssh2
```

`deploy` heeft `*` als wachtwoord — een "Accepted password" voor zo'n account
is het **exacte compromis-indicator** uit de SSHole-disclosure (sectie 6).

### 8.6 Mitigatie bevestigen

Het `sshole-secure`-doel laat de mitigatie zien: met Alpine's gepatchte
openssh-pakket én `PasswordAuthentication no` (sectie 6) faalt de bypass.
Zo demonstreer je de patch-/mitigatie-stap van het practicum.

### 8.7 Opruimen

```sh
docker compose down
```

## 9. Bronnen

- SSHole: https://sshhole.com/
- Alpine Linux Security Advisory: https://alpinelinux.org/posts/2026-11-05-openssh-password-authentication-bypass/
- OpenSSH Release Notes 10.6p2: https://www.openssh.com/releasenotes.html#10.6p2
- GitHub SSHole Lab (leonjza): https://github.com/leonjza/sshhole-lab
- GitHub SSHole Lab (ll1a4x, referentie voor deze lab): https://github.com/ll1a4x/sshhole-lab
- CVE: https://nvd.nist.gov/vuln/detail/CVE-2026-123158