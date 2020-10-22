"""empty message

Revision ID: 3bdfab2b97f9
Revises: 96d9030c0621
Create Date: 2020-10-22 12:35:47.884229

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bdfab2b97f9'
down_revision = '96d9030c0621'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game_player_assoc',
    sa.Column('user_id', sa.String(length=32), nullable=False),
    sa.Column('game_id', sa.String(length=32), nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'game_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('game_player_assoc')
    # ### end Alembic commands ###