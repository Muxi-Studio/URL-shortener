"""empty message

Revision ID: 5ac425de2259
Revises: 
Create Date: 2018-06-07 12:03:29.715363

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5ac425de2259'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    mysql_charset='utf8'
    )
    op.create_index(op.f('ix_roles_default'), 'roles', ['default'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=20), nullable=True),
    sa.Column('is_confirmed', sa.Boolean(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    mysql_charset='utf8'
    )
    op.create_table('urlmaps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('long_url', sa.String(length=200), nullable=True),
    sa.Column('short_code', sa.String(length=20), nullable=True),
    sa.Column('item_type', sa.Boolean(), nullable=True),
    sa.Column('insert_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('available', sa.Boolean(), nullable=True),
    sa.Column('is_locked', sa.Boolean(), nullable=True),
    sa.Column('password', sa.String(length=20), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    mysql_charset='utf8'
    )
    op.create_index(op.f('ix_urlmaps_long_url'), 'urlmaps', ['long_url'], unique=True)
    op.create_index(op.f('ix_urlmaps_short_code'), 'urlmaps', ['short_code'], unique=True)
    op.create_table('statistics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('useragent', sa.String(length=200), nullable=True),
    sa.Column('ip', sa.String(length=50), nullable=True),
    sa.Column('urlmap_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['urlmap_id'], ['urlmaps.id'], ),
    sa.PrimaryKeyConstraint('id'),
    mysql_charset='utf8'
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('statistics')
    op.drop_index(op.f('ix_urlmaps_short_code'), table_name='urlmaps')
    op.drop_index(op.f('ix_urlmaps_long_url'), table_name='urlmaps')
    op.drop_table('urlmaps')
    op.drop_table('users')
    op.drop_index(op.f('ix_roles_default'), table_name='roles')
    op.drop_table('roles')
    # ### end Alembic commands ###
