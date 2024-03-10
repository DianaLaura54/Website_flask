"""empty message

Revision ID: f753942c4aa1
Revises: 4bed7693c230
Create Date: 2024-01-01 14:30:54.778328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f753942c4aa1'
down_revision = '4bed7693c230'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('student', sa.String(length=150), nullable=True))
        batch_op.add_column(sa.Column('donations', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('id_pass', sa.Integer(), nullable=True))
        batch_op.create_unique_constraint(None, ['id_pass'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('id_pass')
        batch_op.drop_column('donations')
        batch_op.drop_column('student')

    # ### end Alembic commands ###
