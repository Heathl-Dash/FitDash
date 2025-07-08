#!/bin/bash

BACKUP_DIR="/backups"
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/full_backup_${POSTGRES_DB}_${DATE}.sql"

pg_dump -U $POSTGRES_USER -d $POSTGRES_DB \
--format=plain \
--create \
--clean \
--if-exists \
--no-owner \
--no-privileges \
--serializable-deferrable \
> $BACKUP_FILE

gzip $BACKUP_FILE

ls -t $BACKUP_DIR/full_backup_${POSTGRES_DB}_*.sql.gz | tail -n +8 | xargs rm -f --