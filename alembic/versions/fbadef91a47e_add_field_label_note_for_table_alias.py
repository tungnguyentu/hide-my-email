"""add field label, note for table alias

Revision ID: fbadef91a47e
Revises: d31ae46188d3
Create Date: 2022-10-09 08:35:48.996543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbadef91a47e'
down_revision = 'd31ae46188d3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('virtual_aliases', sa.Column('label', sa.String(length=200), nullable=False))
    op.add_column('virtual_aliases', sa.Column('note', sa.String(length=1000), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('virtual_aliases', 'note')
    op.drop_column('virtual_aliases', 'label')
    # ### end Alembic commands ###
