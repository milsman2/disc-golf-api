#!/usr/bin/env bash

set -e
set -x

# Load environment variables from .env if it exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Echo connection details for debugging
echo "=== PostgreSQL Connection Details ==="
echo "POSTGRES_SERVER: $POSTGRES_SERVER"
echo "POSTGRES_PORT: $POSTGRES_PORT"
echo "POSTGRES_USER: $POSTGRES_USER"
echo "POSTGRES_DB: $POSTGRES_DB"
echo "POSTGRES_OWNER: $POSTGRES_OWNER"
echo "====================================="

echo "Attempting to connect to: $POSTGRES_SERVER:$POSTGRES_PORT as user $POSTGRES_OWNER"

until pg_isready -h "$POSTGRES_SERVER" -p "$POSTGRES_PORT" -U "$POSTGRES_OWNER"; do
  echo "Waiting for Postgres... (trying $POSTGRES_SERVER:$POSTGRES_PORT)"
  sleep 1
done

# Use postgres superuser to create the database and owner
if PGPASSWORD="$POSTGRES_PASSWORD" \
    psql -h "$POSTGRES_SERVER" -p "$POSTGRES_PORT" \
    -U postgres -lqt | cut -d \| -f 1 | grep -qw "$POSTGRES_DB"; then
    echo "Database $POSTGRES_DB already exists."
else
    echo "Database $POSTGRES_DB not found. Creating..."
    echo "Attempting to connect as postgres user with password: $POSTGRES_PASSWORD"
    # Create the owner role if it doesn't exist
    PGPASSWORD="$POSTGRES_PASSWORD" \
        psql -h "$POSTGRES_SERVER" -p "$POSTGRES_PORT" \
        -U postgres -c "DO \$\$ BEGIN IF NOT EXISTS \
        (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$POSTGRES_OWNER') \
        THEN CREATE ROLE \"$POSTGRES_OWNER\" WITH LOGIN CREATEDB; END IF; END \$\$;"
    # Create the database owned by POSTGRES_OWNER
    PGPASSWORD="$POSTGRES_PASSWORD" \
        createdb -h "$POSTGRES_SERVER" -p "$POSTGRES_PORT" \
        -U postgres -O "$POSTGRES_OWNER" -T template1 "$POSTGRES_DB"
fi

# Create admin user in the new database using POSTGRES_USER
PGPASSWORD="$POSTGRES_PASSWORD" \
    psql -h "$POSTGRES_SERVER" -p "$POSTGRES_PORT" \
    -U "$POSTGRES_OWNER" -d "$POSTGRES_DB" \
    -c "DO \$\$ BEGIN IF NOT EXISTS \
    (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$POSTGRES_USER') \
    THEN CREATE ROLE \"$POSTGRES_USER\" WITH LOGIN SUPERUSER CREATEDB \
    CREATEROLE INHERIT NOREPLICATION PASSWORD '$POSTGRES_PASSWORD'; \
    END IF; END \$\$;"

# Let the DB start
python -m src.pre_start

# Run migrations
alembic upgrade head

# Create initial data in DB
python -m src.initial_data