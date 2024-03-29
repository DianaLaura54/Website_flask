"""empty message

Revision ID: 60ae2b6fcd56
Revises: 94b62bb8da72
Create Date: 2024-01-01 18:23:07.231745

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60ae2b6fcd56'
down_revision = '94b62bb8da72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pass', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_pass', sa.Integer(), nullable=False))
        batch_op.drop_column('id')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'pass', ['id_pass'], ['id_pass'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    with op.batch_alter_table('pass', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), nullable=False))
        batch_op.drop_column('id_pass')

    # ### end Alembic commands ###
