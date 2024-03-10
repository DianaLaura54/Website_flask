"""empty message

Revision ID: 48cce762e270
Revises: edacd18e3390
Create Date: 2024-01-01 20:28:54.648741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48cce762e270'
down_revision = 'edacd18e3390'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'pass', ['id_pass'], ['id_pass'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
