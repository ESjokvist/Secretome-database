"""Added taxonomy database

Revision ID: 70713f13acdc
Revises: fb026f3d6a41
Create Date: 2016-02-17 11:53:30.524040

"""

# revision identifiers, used by Alembic.
revision = '70713f13acdc'
down_revision = 'fb026f3d6a41'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('taxonomies',
    sa.Column('id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('specie_id', sa.Integer(), nullable=True),
    sa.Column('no_rank', sa.String(), nullable=True),
    sa.Column('varietas', sa.String(), nullable=True),
    sa.Column('species', sa.String(), nullable=True),
    sa.Column('genus', sa.String(), nullable=True),
    sa.Column('family', sa.String(), nullable=True),
    sa.Column('order', sa.String(), nullable=True),
    sa.Column('t_class', sa.String(), nullable=True),
    sa.Column('phylum', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['specie_id'], ['species.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column(u'species', sa.Column('current_name', sa.String(), nullable=True))
    op.add_column(u'species', sa.Column('taxon', sa.String(), nullable=True))
    op.drop_column(u'species', 'taxon_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'species', sa.Column('taxon_id', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column(u'species', 'taxon')
    op.drop_column(u'species', 'current_name')
    op.drop_table('taxonomies')
    ### end Alembic commands ###
