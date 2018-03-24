#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
COMPOSE_FILE="$DIR/docker-compose.yml"
docker-compose -f $COMPOSE_FILE $@