"""empty message

Revision ID: d8cbf5acfcaf
Revises: 877daed3ee1d
Create Date: 2024-03-16 18:56:53.053809

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8cbf5acfcaf'
down_revision = '877daed3ee1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('seance', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cours_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('salle_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('professeur_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_seance_professeur_id_professeur'), 'professeur', ['professeur_id'], ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_seance_cours_id_cours'), 'cours', ['cours_id'], ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_seance_salle_id_salle'), 'salle', ['salle_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('seance', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_seance_salle_id_salle'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_seance_cours_id_cours'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_seance_professeur_id_professeur'), type_='foreignkey')
        batch_op.drop_column('professeur_id')
        batch_op.drop_column('salle_id')
        batch_op.drop_column('cours_id')

    # ### end Alembic commands ###