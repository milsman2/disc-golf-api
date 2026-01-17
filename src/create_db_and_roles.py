"""
Database and role creation utility for PostgreSQL environments.
Run this script only when provisioning a new environment or database.
"""

import psycopg
from icecream import ic
from psycopg import sql

from src.core import settings


def create_db():
    admin_conn = psycopg.connect(
        host=settings.POSTGRES_SERVER,
        port=settings.POSTGRES_PORT,
        user=settings.POSTGRES_OWNER,
        password=settings.POSTGRES_PASSWORD,
        dbname=settings.POSTGRES_DB,
        autocommit=True,
    )
    cur = admin_conn.cursor()
    cur.execute("SELECT 1 FROM pg_roles WHERE rolname=%s", (settings.POSTGRES_OWNER,))
    if not cur.fetchone():
        cur.execute(
            sql.SQL("CREATE ROLE {} WITH LOGIN CREATEDB").format(
                sql.Identifier(settings.POSTGRES_OWNER)
            )
        )
    cur.execute("SELECT 1 FROM pg_database WHERE datname=%s", (settings.POSTGRES_DB,))
    if not cur.fetchone():
        cur.execute(
            sql.SQL("CREATE DATABASE {} OWNER {} TEMPLATE template1").format(
                sql.Identifier(settings.POSTGRES_DB),
                sql.Identifier(settings.POSTGRES_OWNER),
            )
        )
    cur.close()
    admin_conn.close()
    ic("Database created (if not already present)")


def create_roles():
    db_conn = psycopg.connect(
        host=settings.POSTGRES_SERVER,
        port=settings.POSTGRES_PORT,
        user=settings.POSTGRES_OWNER,
        password=settings.POSTGRES_PASSWORD,
        dbname=settings.POSTGRES_DB,
        autocommit=True,
    )
    cur = db_conn.cursor()
    cur.execute("SELECT 1 FROM pg_roles WHERE rolname=%s", (settings.POSTGRES_USER,))
    if not cur.fetchone():
        cur.execute(
            sql.SQL(
                "CREATE ROLE {} WITH LOGIN SUPERUSER CREATEDB "
                "CREATEROLE INHERIT NOREPLICATION PASSWORD %s"
            ).format(sql.Identifier(settings.POSTGRES_USER)),
            [settings.POSTGRES_PASSWORD],
        )
    cur.close()
    db_conn.close()
    ic("Roles created (if not already present)")


def main():
    create_db()
    create_roles()
    ic("DB and roles creation complete")


if __name__ == "__main__":
    main()
