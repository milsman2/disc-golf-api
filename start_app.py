"""
Combined pre_start and app launch script for container entrypoint
"""

import subprocess
import sys
import time

import psycopg
from psycopg import sql
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.theme import Theme

from src.core import settings

custom_theme = Theme(
    {
        "neon_purple": "bold magenta",
        "neon_turquoise": "bold cyan",
        "neon_border": "bold magenta",
        "neon_accent": "bold cyan",
        "neon_wait": "bold magenta on black",
        "neon_success": "bold cyan on black",
    }
)
console = Console(theme=custom_theme)


def echo_env():
    details = (
        f"[neon_accent]POSTGRES_SERVER:[/] [neon_purple]{settings.POSTGRES_SERVER}[/]\n"
        f"[neon_accent]POSTGRES_PORT:[/] [neon_purple]{settings.POSTGRES_PORT}[/]\n"
        f"[neon_accent]POSTGRES_USER:[/] [neon_purple]{settings.POSTGRES_USER}[/]\n"
        f"[neon_accent]POSTGRES_DB:[/] [neon_purple]{settings.POSTGRES_DB}[/]\n"
        f"[neon_accent]POSTGRES_OWNER:[/] [neon_purple]{settings.POSTGRES_OWNER}[/]"
    )
    panel = Panel(
        details,
        title="[neon_turquoise]PostgreSQL Connection Details[/]",
        border_style="neon_border",
        subtitle="[neon_turquoise]Synthwave DB Boot[/]",
        padding=(1, 2),
    )
    console.print(panel)


def wait_for_postgres():
    host = settings.POSTGRES_SERVER
    port = settings.POSTGRES_PORT
    user = settings.POSTGRES_OWNER
    password = settings.POSTGRES_PASSWORD
    db = settings.POSTGRES_DB
    while True:
        try:
            conn = psycopg.connect(
                host=host,
                port=5432,
                user=user,
                password=password,
                dbname=db,
                connect_timeout=2,
            )
            conn.close()
            console.print(
                Text(
                    f"[✓] Connected to Postgres at {host}:{port} (DB: {db})",
                    style="neon_success",
                )
            )
            break
        except psycopg.OperationalError as e:
            console.print(
                Text(
                    "[⏳] Waiting for Postgres... "
                    f"(trying {host}:{port}, DB: {db}) - {e}",
                    style="neon_wait",
                )
            )
            time.sleep(1)


def create_db_and_roles():
    host = settings.POSTGRES_SERVER
    port = settings.POSTGRES_PORT
    owner = settings.POSTGRES_OWNER
    db = settings.POSTGRES_DB
    user = settings.POSTGRES_USER
    password = settings.POSTGRES_PASSWORD
    admin_conn = psycopg.connect(
        host=host, port=port, user=owner, password=password, dbname=db, autocommit=True
    )
    cur = admin_conn.cursor()
    cur.execute("SELECT 1 FROM pg_roles WHERE rolname=%s", (owner,))
    if not cur.fetchone():
        cur.execute(
            sql.SQL("CREATE ROLE {} WITH LOGIN CREATEDB").format(sql.Identifier(owner))
        )
    cur.execute("SELECT 1 FROM pg_database WHERE datname=%s", (db,))
    if not cur.fetchone():
        cur.execute(
            sql.SQL("CREATE DATABASE {} OWNER {} TEMPLATE template1").format(
                sql.Identifier(db), sql.Identifier(owner)
            )
        )
    cur.close()
    admin_conn.close()

    db_conn = psycopg.connect(
        host=host, port=port, user=owner, password=password, dbname=db, autocommit=True
    )
    cur = db_conn.cursor()
    cur.execute("SELECT 1 FROM pg_roles WHERE rolname=%s", (user,))
    if not cur.fetchone():
        cur.execute(
            sql.SQL(
                "CREATE ROLE {} WITH LOGIN SUPERUSER CREATEDB "
                "CREATEROLE INHERIT NOREPLICATION PASSWORD %s"
            ).format(sql.Identifier(user)),
            [password],
        )
    cur.close()
    db_conn.close()


def run_subprocess(cmd):
    cmd_str = " ".join(cmd)
    console.print(
        Panel(
            f"[neon_turquoise]$ {cmd_str}",
            border_style="neon_border",
            title="[neon_purple]Running Command[/]",
        )
    )
    result = subprocess.run(cmd, check=True)
    return result.returncode


def main():
    echo_env()
    wait_for_postgres()
    create_db_and_roles()
    run_subprocess([sys.executable, "-m", "src.pre_start"])
    run_subprocess(["alembic", "upgrade", "head"])
    run_subprocess([sys.executable, "-m", "src.initial_data"])
    run_subprocess(
        [
            "gunicorn",
            "src.main:app",
            "-w",
            "4",
            "-k",
            "uvicorn.workers.UvicornWorker",
            "--bind",
            "0.0.0.0:8000",
        ]
    )


if __name__ == "__main__":
    main()
