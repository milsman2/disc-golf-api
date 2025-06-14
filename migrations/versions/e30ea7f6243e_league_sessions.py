"""league_sessions

Revision ID: e30ea7f6243e
Revises: d83b9ec34c46
Create Date: 2025-06-03 22:00:20.622086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e30ea7f6243e'
down_revision = 'd83b9ec34c46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('league_sessions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False, comment='Name of the league session'),
    sa.Column('start_date', sa.DateTime(), nullable=False, comment='Start date of the league session'),
    sa.Column('end_date', sa.DateTime(), nullable=False, comment='End date of the league session'),
    sa.Column('description', sa.String(length=255), nullable=True, comment='Description of the league session'),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_league_sessions'))
    )
    op.create_index(op.f('ix_league_sessions_id'), 'league_sessions', ['id'], unique=False)
    op.create_index(op.f('ix_league_sessions_name'), 'league_sessions', ['name'], unique=False)
    op.add_column('event_results', sa.Column('league_session_id', sa.Integer(), nullable=False))
    op.alter_column('event_results', 'round_points',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               existing_nullable=False)
    op.create_foreign_key(op.f('fk_event_results_league_session_id_league_sessions'), 'event_results', 'league_sessions', ['league_session_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_event_results_league_session_id_league_sessions'), 'event_results', type_='foreignkey')
    op.alter_column('event_results', 'round_points',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.drop_column('event_results', 'league_session_id')
    op.drop_index(op.f('ix_league_sessions_name'), table_name='league_sessions')
    op.drop_index(op.f('ix_league_sessions_id'), table_name='league_sessions')
    op.drop_table('league_sessions')
    # ### end Alembic commands ###
