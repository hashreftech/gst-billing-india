"""Add custom_fields JSON columns to all tables

Revision ID: b9386c636d88
Revises: 60d636098e47
Create Date: 2025-07-28 11:01:37.567178

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON


# revision identifiers, used by Alembic.
revision = 'b9386c636d88'
down_revision = '60d636098e47'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add custom_fields column to users table
    op.add_column('users', sa.Column('custom_fields', JSON, nullable=True, server_default='{}'))
    
    # Add custom_fields column to category table
    op.add_column('category', sa.Column('custom_fields', JSON, nullable=True, server_default='{}'))
    
    # Add custom_fields column to bill table
    op.add_column('bill', sa.Column('custom_fields', JSON, nullable=True, server_default='{}'))
    
    # Add custom_fields column to bill_item table
    op.add_column('bill_item', sa.Column('custom_fields', JSON, nullable=True, server_default='{}'))


def downgrade() -> None:
    # Remove custom_fields column from users table
    op.drop_column('users', 'custom_fields')
    
    # Remove custom_fields column from category table
    op.drop_column('category', 'custom_fields')
    
    # Remove custom_fields column from bill table
    op.drop_column('bill', 'custom_fields')
    
    # Remove custom_fields column from bill_item table
    op.drop_column('bill_item', 'custom_fields')
