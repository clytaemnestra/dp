"""empty message

Revision ID: 1cffdac340e1
Revises: fec0b00a1636
Create Date: 2022-05-24 23:18:34.170866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1cffdac340e1'
down_revision = 'fec0b00a1636'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('measure', sa.Column('description', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('measure', 'description')
    # ### end Alembic commands ###