"""initial migration

Revision ID: 220b971b56e6
Revises: cd49b9cac34
Create Date: 2016-08-30 23:23:20.827000

"""

# revision identifiers, used by Alembic.
revision = '220b971b56e6'
down_revision = 'cd49b9cac34'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('roles', sa.Column('default', sa.Boolean(), nullable=True))
    op.add_column('roles', sa.Column('permissions', sa.Integer(), nullable=True))
    op.create_index('ix_roles_default', 'roles', ['default'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_roles_default', 'roles')
    op.drop_column('roles', 'permissions')
    op.drop_column('roles', 'default')
    ### end Alembic commands ###
