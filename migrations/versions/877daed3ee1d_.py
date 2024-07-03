"""empty message

Revision ID: 877daed3ee1d
Revises: e4d431ef8783
Create Date: 2024-03-16 18:53:17.371637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '877daed3ee1d'
down_revision = 'e4d431ef8783'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('absence', schema=None) as batch_op:
        batch_op.add_column(sa.Column('etudiant_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('seance_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(batch_op.f('fk_absence_etudiant_id_etudiant'), 'etudiant', ['etudiant_id'], ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_absence_seance_id_seance'), 'seance', ['seance_id'], ['id'])

    with op.batch_alter_table('annee_scolaire', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_annee_scolaire_libelle'), ['libelle'])

    with op.batch_alter_table('classe', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_classe_libelle'), ['libelle'])

    with op.batch_alter_table('etudiant', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_etudiant_matricule'), ['matricule'])
        batch_op.create_unique_constraint(batch_op.f('uq_etudiant_photo'), ['photo'])

    with op.batch_alter_table('filiere', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_filiere_libelle'), ['libelle'])

    with op.batch_alter_table('module', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_module_libelle'), ['libelle'])

    with op.batch_alter_table('niveau', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_niveau_libelle'), ['libelle'])

    with op.batch_alter_table('professeur', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_professeur_portable'), ['portable'])

    with op.batch_alter_table('role', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_role_libelle'), ['libelle'])

    with op.batch_alter_table('salle', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_salle_libelle'), ['libelle'])

    with op.batch_alter_table('semestre', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_semestre_libelle'), ['libelle'])

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_user_login'), ['login'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_user_login'), type_='unique')

    with op.batch_alter_table('semestre', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_semestre_libelle'), type_='unique')

    with op.batch_alter_table('salle', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_salle_libelle'), type_='unique')

    with op.batch_alter_table('role', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_role_libelle'), type_='unique')

    with op.batch_alter_table('professeur', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_professeur_portable'), type_='unique')

    with op.batch_alter_table('niveau', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_niveau_libelle'), type_='unique')

    with op.batch_alter_table('module', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_module_libelle'), type_='unique')

    with op.batch_alter_table('filiere', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_filiere_libelle'), type_='unique')

    with op.batch_alter_table('etudiant', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_etudiant_photo'), type_='unique')
        batch_op.drop_constraint(batch_op.f('uq_etudiant_matricule'), type_='unique')

    with op.batch_alter_table('classe', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_classe_libelle'), type_='unique')

    with op.batch_alter_table('annee_scolaire', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_annee_scolaire_libelle'), type_='unique')

    with op.batch_alter_table('absence', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_absence_seance_id_seance'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_absence_etudiant_id_etudiant'), type_='foreignkey')
        batch_op.drop_column('seance_id')
        batch_op.drop_column('etudiant_id')

    # ### end Alembic commands ###