"""Added index to Taxonomy

Revision ID: b1bf638c0df9
Revises: 88698767003e
Create Date: 2016-02-22 13:58:54.626561

"""

# revision identifiers, used by Alembic.
revision = 'b1bf638c0df9'
down_revision = '88698767003e'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_taxonomies_id'), 'taxonomies', ['id'], unique=False)
    op.create_index(op.f('ix_taxonomies_phylum'), 'taxonomies', ['phylum'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_taxonomies_phylum'), table_name='taxonomies')
    op.drop_index(op.f('ix_taxonomies_id'), table_name='taxonomies')
    ### end Alembic commands ###
