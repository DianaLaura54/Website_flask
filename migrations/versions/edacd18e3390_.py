"""empty message

Revision ID: edacd18e3390
Revises: 2337793d9019
Create Date: 2024-01-01 19:25:28.746356

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edacd18e3390'
down_revision = '2337793d9019'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_pass')
    with op.batch_alter_table('pass', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_pass', sa.Integer(), nullable=False))
        batch_op.drop_column('id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pass', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.INTEGER(), nullable=False))
        batch_op.drop_column('id_pass')

    op.create_table('_alembic_tmp_pass',
    sa.Column('price', sa.INTEGER(), nullable=True),
    sa.Column('status', sa.VARCHAR(length=150), nullable=True),
    sa.Column('expiration_date', sa.DATETIME(), nullable=True),
    sa.Column('date', sa.DATETIME(), nullable=True),
    sa.Column('id_pass', sa.INTEGER(), nullable=False)
    )
    # ### end Alembic commands ###
