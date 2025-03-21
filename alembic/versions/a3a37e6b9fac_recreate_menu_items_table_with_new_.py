"""Recreate menu_items table with new columns

Revision ID: a3a37e6b9fac
Revises: 0a49533c49f7
Create Date: 2025-03-12 13:24:56.409793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3a37e6b9fac'
down_revision: Union[str, None] = '0a49533c49f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menu_items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.DECIMAL(precision=10, scale=2), nullable=False),
    sa.Column('image_url', sa.String(), nullable=True),
    sa.Column('category', sa.String(), nullable=False),
    sa.Column('is_veg', sa.String(), nullable=False),
    sa.Column('restaurant_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['restaurant_id'], ['restaurants.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_menu_items_id'), 'menu_items', ['id'], unique=False)
    op.create_foreign_key(None, 'menu_item_meal_times', 'menu_items', ['menu_item_id'], ['id'])
    op.create_foreign_key(None, 'orders', 'menu_items', ['item_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'orders', type_='foreignkey')
    op.drop_constraint(None, 'menu_item_meal_times', type_='foreignkey')
    op.drop_index(op.f('ix_menu_items_id'), table_name='menu_items')
    op.drop_table('menu_items')
    # ### end Alembic commands ###
