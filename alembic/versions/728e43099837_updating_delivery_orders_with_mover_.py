"""Updating delivery orders with mover things

Revision ID: 728e43099837
Revises: 46fe802c92e9
Create Date: 2016-12-01 15:59:32.274655

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '728e43099837'
down_revision = '46fe802c92e9'
branch_labels = None
depends_on = None

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('delivery_orders', sa.Column('md5sum_file', sa.String(), nullable=True))
    op.add_column('delivery_orders', sa.Column('mover_delivery_id', sa.String(), nullable=True))
    op.add_column('delivery_orders', sa.Column('mover_pid', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('delivery_orders', 'mover_pid')
    op.drop_column('delivery_orders', 'mover_delivery_id')
    op.drop_column('delivery_orders', 'md5sum_file')
    ### end Alembic commands ###