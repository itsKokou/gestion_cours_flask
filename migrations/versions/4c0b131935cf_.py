"""empty message

Revision ID: 4c0b131935cf
Revises: c4714bc2b330
Create Date: 2024-03-17 13:39:58.662557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c0b131935cf'
down_revision = 'c4714bc2b330'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cours', schema=None) as batch_op:
        batch_op.add_column(sa.Column('nbreHeurePlanifie', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cours', schema=None) as batch_op:
        batch_op.drop_column('nbreHeurePlanifie')

    # ### end Alembic commands ###