"""
Entrypoint script: creates DB/roles, waits for DB, runs migrations, seeds data, then launches the app.
"""

import os
import subprocess
import sys

from rich.console import Console
from rich.panel import Panel
from rich.theme import Theme

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
console = Console(theme=custom_theme, force_terminal=True, width=60)


def echo_env():
    print("\nENVIRONMENT VARIABLES:")
    for k, v in os.environ.items():
        print(f"{k}={v}")
    print()


def run_subprocess(cmd, check=True):
    cmd_str = " ".join(cmd)
    if "console" in globals():
        console.print(
            Panel(
                f"[neon_turquoise]$ {cmd_str}",
                border_style="neon_border",
                title="[neon_purple]Running Command[/]",
                width=80,
                expand=False,
            )
        )
    else:
        print(f"Running: {cmd_str}")
    result = subprocess.run(cmd, check=check)
    return result.returncode


def run_startup_sequence():
    workers = os.environ.get("GUNICORN_WORKERS", "4")
    # 1. Create DB and roles (idempotent)
    run_subprocess([sys.executable, "-m", "src.create_db_and_roles"])
    # 2. Wait for DB readiness
    run_subprocess([sys.executable, "-m", "src.pre_start"])
    # 3. Run migrations
    run_subprocess(["alembic", "upgrade", "head"])
    # 4. Seed initial data
    run_subprocess([sys.executable, "-m", "src.initial_data"])
    # 5. Launch the app
    run_subprocess(
        [
            "gunicorn",
            "src.main:app",
            "-w",
            str(workers),
            "-k",
            "uvicorn.workers.UvicornWorker",
            "--bind",
            "0.0.0.0:8000",
        ]
    )


def main():
    echo_env()
    run_startup_sequence()


if __name__ == "__main__":
    main()
