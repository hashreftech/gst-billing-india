"""Add due_date column to bill table

Revision ID: 52115cb0358c
Revises: b74f1da53ff2
Create Date: 2025-07-28 11:11:20.166667

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Date


# revision identifiers, used by Alembic.
revision = '52115cb0358c'
down_revision = 'b74f1da53ff2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add the due_date column to the bill table
    op.add_column('bill', Column('due_date', Date, nullable=True))


def downgrade() -> None:
    # Remove the due_date column from the bill table
    op.drop_column('bill', 'due_date')
