"""add cgst_rate and sgst_rate columns to product and bill_item tables

Revision ID: 2d6ad5d788bc
Revises: 88d217a7bb7b
Create Date: 2025-07-29 23:02:59.346018

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d6ad5d788bc'
down_revision = '88d217a7bb7b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add cgst_rate and sgst_rate columns to product table
    op.add_column('product', sa.Column('cgst_rate', sa.Numeric(precision=5, scale=2), nullable=False, server_default='9.0'))
    op.add_column('product', sa.Column('sgst_rate', sa.Numeric(precision=5, scale=2), nullable=False, server_default='9.0'))
    
    # Add cgst_rate and sgst_rate columns to bill_item table
    op.add_column('bill_item', sa.Column('cgst_rate', sa.Numeric(precision=5, scale=2), nullable=False, server_default='0.0'))
    op.add_column('bill_item', sa.Column('sgst_rate', sa.Numeric(precision=5, scale=2), nullable=False, server_default='0.0'))
    
    # Update product values to split existing gst_rate in half
    op.execute("""
        UPDATE product 
        SET cgst_rate = gst_rate / 2,
            sgst_rate = gst_rate / 2
    """)
    
    # Update bill_item values to split existing gst_rate in half
    op.execute("""
        UPDATE bill_item 
        SET cgst_rate = gst_rate / 2,
            sgst_rate = gst_rate / 2
    """)


def downgrade() -> None:
    # Remove cgst_rate and sgst_rate columns from bill_item table
    op.drop_column('bill_item', 'cgst_rate')
    op.drop_column('bill_item', 'sgst_rate')
    
    # Remove cgst_rate and sgst_rate columns from product table
    op.drop_column('product', 'cgst_rate')
    op.drop_column('product', 'sgst_rate')
