"""empty message

Revision ID: c67b62e8cace
Revises: 07435892867a
Create Date: 2024-01-04 01:38:52.145455

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c67b62e8cace'
down_revision = '07435892867a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('book_id', sa.Integer(), nullable=False))
        batch_op.alter_column('status',
               existing_type=sa.BOOLEAN(),
               type_=sa.String(length=150),
               existing_nullable=True)
        batch_op.drop_column('id')

    with op.batch_alter_table('pass', schema=None) as batch_op:
        batch_op.drop_column('expiration_date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pass', schema=None) as batch_op:
        batch_op.add_column(sa.Column('expiration_date', sa.DATE(), nullable=True))

    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), nullable=False))
        batch_op.alter_column('status',
               existing_type=sa.String(length=150),
               type_=sa.BOOLEAN(),
               existing_nullable=True)
        batch_op.drop_column('book_id')

    # ### end Alembic commands ###