"""Fix bill and bill_item table schema

Revision ID: 88d217a7bb7b
Revises: 52115cb0358c
Create Date: 2025-07-28 11:12:42.352724

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Numeric, String, Text


# revision identifiers, used by Alembic.
revision = '88d217a7bb7b'
down_revision = '52115cb0358c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add missing columns to bill table
    op.add_column('bill', Column('subtotal', Numeric(12, 2), nullable=False, server_default='0'))
    op.add_column('bill', Column('discount_type', String(10), nullable=True, server_default='none'))
    op.add_column('bill', Column('discount_value', Numeric(12, 2), nullable=True, server_default='0'))
    op.add_column('bill', Column('sgst_amount', Numeric(12, 2), nullable=False, server_default='0'))
    op.add_column('bill', Column('cgst_amount', Numeric(12, 2), nullable=False, server_default='0'))
    op.add_column('bill', Column('igst_amount', Numeric(12, 2), nullable=False, server_default='0'))
    
    # Add missing columns to bill_item table
    op.add_column('bill_item', Column('description', Text, nullable=True))
    op.add_column('bill_item', Column('unit', String(20), nullable=True, server_default='Nos'))
    op.add_column('bill_item', Column('rate', Numeric(10, 2), nullable=False, server_default='0'))
    op.add_column('bill_item', Column('amount', Numeric(12, 2), nullable=False, server_default='0'))
    op.add_column('bill_item', Column('sgst_amount', Numeric(12, 2), nullable=False, server_default='0'))
    op.add_column('bill_item', Column('cgst_amount', Numeric(12, 2), nullable=False, server_default='0'))
    op.add_column('bill_item', Column('igst_amount', Numeric(12, 2), nullable=False, server_default='0'))


def downgrade() -> None:
    # Remove added columns from bill table
    op.drop_column('bill', 'subtotal')
    op.drop_column('bill', 'discount_type')
    op.drop_column('bill', 'discount_value')
    op.drop_column('bill', 'sgst_amount')
    op.drop_column('bill', 'cgst_amount')
    op.drop_column('bill', 'igst_amount')
    
    # Remove added columns from bill_item table
    op.drop_column('bill_item', 'description')
    op.drop_column('bill_item', 'unit')
    op.drop_column('bill_item', 'rate')
    op.drop_column('bill_item', 'amount')
    op.drop_column('bill_item', 'sgst_amount')
    op.drop_column('bill_item', 'cgst_amount')
    op.drop_column('bill_item', 'igst_amount')
