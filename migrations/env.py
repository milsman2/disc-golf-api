"""
Alembic environment configuration file.
"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from src.core import Base, settings

import re

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def get_url() -> str:
    return str(settings.sql_alchemy_db_uri)


url = get_url()
config.set_main_option("sqlalchemy.url", url)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    db_url = config.get_main_option("sqlalchemy.url")
    if re.search(r"\sqlite", url, re.IGNORECASE):
        context.configure(
            url=db_url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
            render_as_batch=True,
        )
    else:
        context.configure(
            url=db_url,
            target_metadata=target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
        )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_engine(
        url,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as conn:
        if re.search(r"\sqlite", url, re.IGNORECASE):
            context.configure(
                connection=conn,
                target_metadata=target_metadata,
                render_as_batch=True,
            )
        else:
            context.configure(
                connection=conn,
                target_metadata=target_metadata,
            )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
