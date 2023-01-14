"""empty message

Revision ID: 71f00b004c95
Revises: 9e9f454aeca5
Create Date: 2023-01-14 15:46:28.918490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71f00b004c95'
down_revision = '9e9f454aeca5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.drop_column('types')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('characters', schema=None) as batch_op:
        batch_op.add_column(sa.Column('types', sa.VARCHAR(length=80), autoincrement=False, nullable=True))

    # ### end Alembic commands ###