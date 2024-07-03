"""empty message

Revision ID: c4714bc2b330
Revises: 9b4b9c3dea33
Create Date: 2024-03-17 10:44:19.827665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4714bc2b330'
down_revision = '9b4b9c3dea33'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('declaration',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('motif', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('seance_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['seance_id'], ['seance.id'], name=op.f('fk_declaration_seance_id_seance')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_declaration_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_declaration'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('declaration')
    # ### end Alembic commands ###
