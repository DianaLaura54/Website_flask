"""empty message

Revision ID: 1ebfdf277f57
Revises: 58a67b7e503e
Create Date: 2024-01-01 14:55:09.062907

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ebfdf277f57'
down_revision = '58a67b7e503e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_pass', sa.Integer(), nullable=True))
        batch_op.drop_column('age')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('age', sa.INTEGER(), nullable=True))
        batch_op.drop_column('id_pass')

    # ### end Alembic commands ###
