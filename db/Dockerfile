FROM postgres:11

RUN set -x \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y postgis postgresql-11-postgis-2.5

# locales are broken for the base image, for god-knows-what reason
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y locales \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && dpkg-reconfigure --frontend=noninteractive locales \
    && update-locale LANG=en_US.UTF-8

ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

EXPOSE 5432

