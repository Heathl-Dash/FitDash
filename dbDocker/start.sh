#!/bin/bash
set -e

chmod +x /docker-entrypoint-initdb.d/backup_script.sh

echo "0 0 * * * root /docker-entrypoint-initdb.d/backup_script.sh >> /var/log/cron.log 2>&1" >> /etc/crontab
echo "0 3 * * 0 root /usr/local/bin/scripts/refresh_view.sh >> /var/log/cron.log 2>&1" >> /etc/crontab

service cron start
/bin/bash /usr/local/bin/create_mv_init.sh  2>&1 &

exec docker-entrypoint.sh postgres
