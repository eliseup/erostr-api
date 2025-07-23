#!/bin/bash
set -e

PROGRAM=$1

# Start supervisor
supervisord -c /etc/supervisor/supervisord.conf &

# Wait for supervisor socket
sleep 2

# Start only the chosen program
supervisorctl start "$PROGRAM"

# Wait for supervisord (foreground wait)
wait %1
