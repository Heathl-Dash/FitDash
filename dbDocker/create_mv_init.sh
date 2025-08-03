#!/bin/bash
set -e

sleep 20
DB_HOST="localhost"
DB_PORT="${DB_PORT:-5432}" 
DB_USER="${POSTGRES_USER}"
DB_NAME="${POSTGRES_DB}"
PG_PASS="${POSTGRES_PASSWORD}"
SQL_SCRIPT="/usr/local/bin/scripts/create_mv.sql" 
echo "INFO: DB_NAME = $DB_NAME"
MAX_ATTEMPTS=60
SLEEP_TIME=5 

echo "INFO: [MV_INIT] Script de inicialização da Materialized View iniciado."
echo "INFO: [MV_INIT] Tentando criar Materialized Views a partir de $SQL_SCRIPT"


i=1
while [ "$i" -le "$MAX_ATTEMPTS" ]; do
    echo "INFO: [MV_INIT] Tentativa $i de $MAX_ATTEMPTS para criar MVs."

    if pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" > /dev/null 2>&1 && \
       PGPASSWORD="$PG_PASS" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "$SQL_SCRIPT" > /dev/null 2>&1; then
        echo "SUCCESS: [MV_INIT] Materialized Views criadas com sucesso."
        exit 0
    else
        echo "WARNING: [MV_INIT] Falha na criação das MVs ou DB não pronto. Aguardando $SLEEP_TIME segundos..."
        sleep "$SLEEP_TIME"
    fi

    i=$((i+1))
done

echo "ERROR: [MV_INIT] Excedido o número máximo de tentativas para criar Materialized Views. Falha na criação."
exit 1 