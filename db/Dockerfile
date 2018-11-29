FROM postgres:11

RUN set -x \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y postgis postgresql-11-postgis-2.5

EXPOSE 5432

