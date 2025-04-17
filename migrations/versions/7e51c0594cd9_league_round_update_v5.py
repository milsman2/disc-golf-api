"""league_round_update_v5

Revision ID: 7e51c0594cd9
Revises: a673fefa5c96
Create Date: 2025-04-12 14:34:14.162152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e51c0594cd9'
down_revision = 'a673fefa5c96'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event_results', schema=None) as batch_op:
        batch_op.alter_column('position_raw',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event_results', schema=None) as batch_op:
        batch_op.alter_column('position_raw',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
