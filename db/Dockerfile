FROM postgres:9.4

RUN set -x \
    && apt-get update \
    && apt-get upgrade -y \
&& apt-get install -y postgis postgresql-9.4-postgis-2.1

COPY ./data /docker-entrypoint-initdb.d/