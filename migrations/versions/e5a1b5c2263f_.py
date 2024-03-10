"""empty message

Revision ID: e5a1b5c2263f
Revises: df7392a196ac
Create Date: 2024-01-01 14:58:52.548321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5a1b5c2263f'
down_revision = 'df7392a196ac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_pass', sa.Integer(), nullable=True))
        batch_op.create_unique_constraint(None, ['id_pass'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('id_pass')

    # ### end Alembic commands ###
