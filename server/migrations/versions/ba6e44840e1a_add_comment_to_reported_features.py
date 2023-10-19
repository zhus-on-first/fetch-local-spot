"""add comment to reported_features

Revision ID: ba6e44840e1a
Revises: 185510e16918
Create Date: 2023-10-19 09:49:04.193771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba6e44840e1a'
down_revision = '185510e16918'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reported_features', schema=None) as batch_op:
        batch_op.add_column(sa.Column('comment', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reported_features', schema=None) as batch_op:
        batch_op.drop_column('comment')

    # ### end Alembic commands ###