#!/bin/bash
set -e
ip=<YOUR_IP>
# export DISPLAY="$(echo -e "$(hostname -I):0.0" | tr -d '[:space:]')"
export DISPLAY="$ip:0"
exec "$@"

