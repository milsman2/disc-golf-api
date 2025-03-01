#! /usr/bin/env bash

set -e
set -x

# Let the DB start
python -m src.pre_start

# Run migrations
alembic upgrade head

# Create initial data in DB
python -m src.initial_data