"""empty message

Revision ID: 2c76cdcc9a4c
Revises: be3f427eda09
Create Date: 2024-01-03 01:41:16.554003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c76cdcc9a4c'
down_revision = 'be3f427eda09'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pass', schema=None) as batch_op:
        batch_op.alter_column('expiration_date',
               existing_type=sa.DATETIME(),
               type_=sa.Date(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pass', schema=None) as batch_op:
        batch_op.alter_column('expiration_date',
               existing_type=sa.Date(),
               type_=sa.DATETIME(),
               existing_nullable=True)

    # ### end Alembic commands ###
