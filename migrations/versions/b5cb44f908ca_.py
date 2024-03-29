"""empty message

Revision ID: b5cb44f908ca
Revises: 7c005a9a1bc5
Create Date: 2024-01-03 18:04:29.548238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5cb44f908ca'
down_revision = '7c005a9a1bc5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_column('copies')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('copies', sa.INTEGER(), nullable=True))

    # ### end Alembic commands ###
