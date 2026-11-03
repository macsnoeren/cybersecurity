# PHP under Apache mod_php for a local security-research lab.
#
# The php:*-apache images ship Apache httpd with mod_php already wired in (the
# "apache2handler" SAPI) -- the classic mod_php setup.
#
# docker-compose.yml passes PHP_VERSION=8.3.35-apache, a PRE-FIX release, so
# `docker compose up --build` gives a lab that IS vulnerable to PHP2Shell
# (CVE-2026-109618 / CVE-2026-109619, fixed in 8.2.35 / 8.3.36 / 8.4.27 /
# 8.5.12). The ARG default below (patched 8.3) only applies to a plain
# `docker build`. For a patched lab via Compose:
#
#     PHP_VERSION=8.3-apache docker compose up --build
#
# A pre-fix build is intentionally insecure and must never touch a real network.
# See README.md. Visit /php2shell.php in the lab to see which state you are in.
ARG PHP_VERSION=8.3-apache
FROM php:${PHP_VERSION}

# Make the running configuration easy to inspect from inside the lab.
RUN { \
      echo "expose_php = On"; \
      echo "display_errors = On"; \
      echo "display_startup_errors = On"; \
      echo "error_reporting = E_ALL"; \
      echo "date.timezone = UTC"; \
    } > /usr/local/etc/php/conf.d/zz-lab.ini

# The simple PHP page(s) that make up the lab front-end.
COPY www/ /var/www/html/

# mod_php runs as the apache user; give it the document root.
RUN chown -R www-data:www-data /var/www/html

EXPOSE 80
