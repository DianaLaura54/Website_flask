"""empty message

Revision ID: df7392a196ac
Revises: fb2043016cd4
Create Date: 2024-01-01 14:58:13.722929

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df7392a196ac'
down_revision = 'fb2043016cd4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('age', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('donations', sa.Integer(), nullable=True))
        batch_op.drop_column('id_pass')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_pass', sa.INTEGER(), nullable=True))
        batch_op.drop_column('donations')
        batch_op.drop_column('age')

    # ### end Alembic commands ###
