"""Initial Migration

Revision ID: 8724ff7c15c5
Revises: 
Create Date: 2024-01-23 23:47:59.214259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8724ff7c15c5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=200), nullable=False),
    sa.Column('last_name', sa.String(length=200), nullable=False),
    sa.Column('email', sa.String(length=200), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('login_attempts', sa.Integer(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('account_type', sa.Enum('USER', 'ADMIN', 'SUPER_ADMIN', name='accounttype'), nullable=True),
    sa.Column('date_created', sa.Date(), nullable=True),
    sa.Column('date_updated', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_email'))

    op.drop_table('users')
    # ### end Alembic commands ###
