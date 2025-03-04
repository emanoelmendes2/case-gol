"""Criação das tabelas

Revision ID: 283c23b342de
Revises: 
Create Date: 2025-03-03 21:06:55.755020

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '283c23b342de'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('voo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ano', sa.Integer(), nullable=False),
    sa.Column('mes', sa.Integer(), nullable=False),
    sa.Column('mercado', sa.String(length=10), nullable=False),
    sa.Column('rpk', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('voo')
    op.drop_table('usuario')
    # ### end Alembic commands ###
