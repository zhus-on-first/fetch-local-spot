"""add cascade delete to Report class method

Revision ID: 93ed8acdbd2a
Revises: 532802755a89
Create Date: 2023-10-30 19:27:25.289192

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93ed8acdbd2a'
down_revision = '532802755a89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('features', schema=None) as batch_op:
        batch_op.create_unique_constraint('uq_features_name', ['name'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('features', schema=None) as batch_op:
        batch_op.drop_constraint('uq_features_name', type_='unique')

    # ### end Alembic commands ###
