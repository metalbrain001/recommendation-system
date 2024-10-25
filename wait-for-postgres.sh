#!/bin/sh

# wait-for-postgres.sh
POSTGRES_HOST=${PG_HOST:-"metalbrain"}
PG_PORT=${PG_PORT:-"5432"}
MAX_ATTEMPTS=${MAX_ATTEMPTS:-"10"}
SLEEP_INTERVAL=${SLEEP_INTERVAL:-"5"}
RETRIES=0

while ! pg_ready -h $PG_HOST -p $PG_PORT > /dev/null 2>&1; do
  RETRIES=$((RETRIES+1))
  if [ $RETRIES -eq $MAX_ATTEMPTS ]; then
    echo "Max retries reached"
    exit 1
  fi
  echo "Waiting for postgres on $PG_HOST:$PG_PORT... ($RETRIES/$MAX_ATTEMPTS)"
  sleep $SLEEP_INTERVAL
done

echo "Postgres is ready!"
pg_ready -h $POSTGRES_HOST -p $PG_PORT

 The script above is a simple shell script that waits for the Postgres database to be ready before starting the application. It uses the  pg_ready  command to check if the database is ready. The script will wait for the database to be ready for a maximum of 10 attempts with a sleep interval of 5 seconds between each attempt.
 The  pg_ready  command is a simple utility that checks if the Postgres database is ready. You can download the  pg_ready  utility from  here.
 Make the script executable:
 $ chmod +x wait-for-postgres.sh

 Now, you can use the script in your Dockerfile to wait for the Postgres database to be ready before starting the application.
 Here is an example Dockerfile that uses the  wait-for-postgres.sh  script: