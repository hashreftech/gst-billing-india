"""Add custom_fields column

Revision ID: 60d636098e47
Revises: 1feb3a351dc1
Create Date: 2025-07-28 09:36:41.893922

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision = '60d636098e47'
down_revision = '1feb3a351dc1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add custom_fields column to product table
    op.add_column('product', sa.Column('custom_fields', JSONB, nullable=True, server_default='{}'))
    
    # Add custom_fields column to customer table
    op.add_column('customer', sa.Column('custom_fields', JSONB, nullable=True, server_default='{}'))
    
    # Add custom_fields column to company_config table
    op.add_column('company_config', sa.Column('custom_fields', JSONB, nullable=True, server_default='{}'))


def downgrade() -> None:
    # Remove custom_fields column from product table
    op.drop_column('product', 'custom_fields')
    
    # Remove custom_fields column from customer table
    op.drop_column('customer', 'custom_fields')
    
    # Remove custom_fields column from company_config table
    op.drop_column('company_config', 'custom_fields')
