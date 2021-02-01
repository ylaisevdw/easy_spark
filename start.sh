#!/bin/bash
set -e
export DISPLAY="host.docker.internal:0.0"
exec "$@"

