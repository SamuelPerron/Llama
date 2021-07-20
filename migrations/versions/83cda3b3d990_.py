"""empty message

Revision ID: 83cda3b3d990
Revises: fa488babce7b
Create Date: 2021-05-22 00:54:14.672739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83cda3b3d990'
down_revision = 'fa488babce7b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'positions', sa.Column('_lastday_price', sa.Float(), nullable=True)
    )
    op.add_column(
        'positions',
        sa.Column('_lastday_price_last_check', sa.DateTime(), nullable=True),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('positions', '_lastday_price_last_check')
    op.drop_column('positions', '_lastday_price')
    # ### end Alembic commands ###