"""renamed species field

Revision ID: 77f3cd39f8e7
Revises: 092b93bc3a73
Create Date: 2016-02-17 13:44:38.678234

"""

# revision identifiers, used by Alembic.
revision = '77f3cd39f8e7'
down_revision = '092b93bc3a73'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('taxonomies', sa.Column('db_species', sa.String(), nullable=True))
    op.drop_column('taxonomies', 'species')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('taxonomies', sa.Column('species', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('taxonomies', 'db_species')
    ### end Alembic commands ###
