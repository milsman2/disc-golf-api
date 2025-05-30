"""league_round_update_v4

Revision ID: a673fefa5c96
Revises: 95b51638aaad
Create Date: 2025-04-10 15:19:56.056766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a673fefa5c96'
down_revision = '95b51638aaad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event_results', schema=None) as batch_op:
        batch_op.alter_column('position_raw',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_constraint('fk_event_results_course_id_courses', type_='foreignkey')
        batch_op.drop_column('course_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event_results', schema=None) as batch_op:
        batch_op.add_column(sa.Column('course_id', sa.INTEGER(), nullable=False))
        batch_op.create_foreign_key('fk_event_results_course_id_courses', 'courses', ['course_id'], ['id'])
        batch_op.alter_column('position_raw',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
