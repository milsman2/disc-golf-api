#! /usr/bin/env bash

set -e
set -x

# Load environment variables from .env if it exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

until pg_isready -h "$POSTGRES_SERVER" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  echo "Waiting for Postgres..."
  sleep 1
done

# Use postgres superuser to create the database and owner
if PGPASSWORD="$POSTGRES_PASSWORD" \
    psql -h "$POSTGRES_SERVER" -p "$POSTGRES_PORT" \
    -U postgres -lqt | cut -d \| -f 1 | grep -qw "$POSTGRES_DB"; then
    echo "Database $POSTGRES_DB already exists."
else
    echo "Database $POSTGRES_DB not found. Creating..."
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