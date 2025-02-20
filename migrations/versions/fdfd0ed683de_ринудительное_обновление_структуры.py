"""ринудительное обновление структуры

Revision ID: fdfd0ed683de
Revises: aadc39958d77
Create Date: 2025-02-20 01:08:36.588545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fdfd0ed683de'
down_revision = 'aadc39958d77'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cashier', schema=None) as batch_op:
        batch_op.alter_column('store',
               existing_type=sa.TEXT(),
               type_=sa.String(length=50),
               nullable=False,
               existing_server_default=sa.text("'kanimex'"))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cashier', schema=None) as batch_op:
        batch_op.alter_column('store',
               existing_type=sa.String(length=50),
               type_=sa.TEXT(),
               nullable=True,
               existing_server_default=sa.text("'kanimex'"))

    # ### end Alembic commands ###
