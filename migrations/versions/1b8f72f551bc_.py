"""empty message

Revision ID: 1b8f72f551bc
Revises: 6ccda8950bfa
Create Date: 2018-10-28 16:23:09.747604

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1b8f72f551bc'
down_revision = '6ccda8950bfa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('movies', 'rating')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movies', sa.Column('rating', mysql.SMALLINT(display_width=6), autoincrement=False, nullable=True))
    # ### end Alembic commands ###