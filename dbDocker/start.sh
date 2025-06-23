#!/bin/bash
set -e

chmod +x /docker-entrypoint-initdb.d/backup_script.sh

echo "* * * * * root /docker-entrypoint-initdb.d/backup_script.sh >> /var/log/cron.log 2>&1" >> /etc/crontab

service cron start

exec docker-entrypoint.sh postgres
