"""propelauth integration make some user fields optional

Revision ID: 98985b7122ca
Revises: 49b315816710
Create Date: 2023-11-08 23:02:05.416737

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '98985b7122ca'
down_revision = '49b315816710'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=10),
               nullable=True)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=40),
               nullable=True)
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=40),
               nullable=False)
        batch_op.alter_column('username',
               existing_type=sa.VARCHAR(length=10),
               nullable=False)

    # ### end Alembic commands ###