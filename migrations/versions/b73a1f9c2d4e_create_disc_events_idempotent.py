"""create disc_events table (idempotent)

Revision ID: b73a1f9c2d4e
Revises: 2940c4327541
Create Date: 2025-10-22 00:00:00.000000

This migration is defensive: it only creates the table/index if they do not
already exist. That avoids DuplicateTable / DuplicateIndex errors when a
partial schema is already present.
"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b73a1f9c2d4e"
down_revision = "2940c4327541"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    # Create table only if it doesn't exist
    if "disc_events" not in inspector.get_table_names():
        op.create_table(
            "disc_events",
            sa.Column(
                "id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False
            ),
            sa.Column("name", sa.String(), nullable=False),
            sa.Column("start_date", sa.DateTime(), nullable=False),
            sa.Column("end_date", sa.DateTime(), nullable=False),
            sa.Column("description", sa.String(), nullable=True),
        )

    # Create index only if it doesn't exist
    if "disc_events" in inspector.get_table_names():
        existing_indexes = {idx["name"] for idx in inspector.get_indexes("disc_events")}
        if (
            op.f("ix_disc_events_id") not in existing_indexes
            and "ix_disc_events_id" not in existing_indexes
        ):
            op.create_index(
                op.f("ix_disc_events_id"), "disc_events", ["id"], unique=False
            )


def downgrade():
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "disc_events" in inspector.get_table_names():
        existing_indexes = {idx["name"] for idx in inspector.get_indexes("disc_events")}
        if (
            op.f("ix_disc_events_id") in existing_indexes
            or "ix_disc_events_id" in existing_indexes
        ):
            op.drop_index(op.f("ix_disc_events_id"), table_name="disc_events")
        op.drop_table("disc_events")
