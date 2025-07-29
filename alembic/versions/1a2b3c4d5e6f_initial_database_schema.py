"""Initial database schema

Revision ID: 1a2b3c4d5e6f
Revises: 
Create Date: 2025-07-28 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1a2b3c4d5e6f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=True),
        sa.Column('last_name', sa.String(length=100), nullable=True),
        sa.Column('phone', sa.String(length=15), nullable=True),
        sa.Column('role', sa.String(length=20), nullable=False, server_default='user'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    
    # Create company_config table
    op.create_table('company_config',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('address', sa.Text(), nullable=False),
        sa.Column('gst_number', sa.String(length=15), nullable=False),
        sa.Column('tan_number', sa.String(length=10), nullable=True),
        sa.Column('state_code', sa.String(length=2), nullable=False),
        sa.Column('logo_path', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create customer table
    op.create_table('customer',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=True),
        sa.Column('phone', sa.String(length=15), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('gst_number', sa.String(length=15), nullable=True),
        sa.Column('state_code', sa.String(length=2), nullable=True),
        sa.Column('is_guest', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create category table
    op.create_table('category',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('category_name', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('category_name')
    )
    
    # Create product table
    op.create_table('product',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('hsn_code', sa.String(length=10), nullable=False),
        sa.Column('gst_rate', sa.Numeric(precision=5, scale=2), nullable=False, server_default='18.0'),
        sa.Column('unit', sa.String(length=20), nullable=False, server_default='Nos'),
        sa.Column('category_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create bill table
    op.create_table('bill',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('bill_number', sa.String(length=20), nullable=False),
        sa.Column('bill_date', sa.Date(), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=True),
        sa.Column('total_amount', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('gst_amount', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('discount_amount', sa.Numeric(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('final_amount', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='draft'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['customer_id'], ['customer.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('bill_number')
    )
    
    # Create bill_item table
    op.create_table('bill_item',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('bill_id', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=True),
        sa.Column('product_name', sa.String(length=200), nullable=False),
        sa.Column('quantity', sa.Numeric(precision=15, scale=3), nullable=False),
        sa.Column('unit_price', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('hsn_code', sa.String(length=10), nullable=False),
        sa.Column('gst_rate', sa.Numeric(precision=5, scale=2), nullable=False),
        sa.Column('discount_percent', sa.Numeric(precision=5, scale=2), nullable=True, server_default='0'),
        sa.Column('discount_amount', sa.Numeric(precision=15, scale=2), nullable=True, server_default='0'),
        sa.Column('taxable_amount', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('gst_amount', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('total_amount', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['bill_id'], ['bill.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['product_id'], ['product.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create field_definition table for dynamic fields
    op.create_table('field_definition',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('field_name', sa.String(length=50), nullable=False),
        sa.Column('display_name', sa.String(length=100), nullable=False),
        sa.Column('field_type', sa.String(length=20), nullable=False),
        sa.Column('required', sa.Boolean(), nullable=True, server_default='false'),
        sa.Column('enabled', sa.Boolean(), nullable=True, server_default='true'),
        sa.Column('field_order', sa.Integer(), nullable=True, server_default='0'),
        sa.Column('options', sa.Text(), nullable=True),
        sa.Column('default_value', sa.Text(), nullable=True),
        sa.Column('validation_regex', sa.Text(), nullable=True),
        sa.Column('help_text', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('entity_type', 'field_name', name='uix_field_entity_name')
    )
    
    # Create field_data table for dynamic field values
    op.create_table('field_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('field_definition_id', sa.Integer(), nullable=False),
        sa.Column('entity_id', sa.Integer(), nullable=False),
        sa.Column('value_text', sa.Text(), nullable=True),
        sa.Column('value_number', sa.Numeric(precision=15, scale=5), nullable=True),
        sa.Column('value_date', sa.DateTime(), nullable=True),
        sa.Column('value_boolean', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['field_definition_id'], ['field_definition.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('field_definition_id', 'entity_id', name='uix_field_entity')
    )
    
    # Create field_definition_history table for tracking changes
    op.create_table('field_definition_history',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('field_definition_id', sa.Integer(), nullable=False),
        sa.Column('change_type', sa.String(length=20), nullable=False),
        sa.Column('changed_by', sa.Integer(), nullable=True),
        sa.Column('old_values', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('new_values', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('changed_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['changed_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['field_definition_id'], ['field_definition.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Insert default data
    op.execute("""
    -- Insert default admin user
    INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_active)
    VALUES ('admin', 'admin@gstbilling.com', 
            '$2b$12$tT4COrBKd9jGADK84h5VWeSaMPTn/6QF1e11/nmQnr8bz.wfQ6xFC', -- admin123
            'System', 'Administrator', 'admin', true);
    
    -- Insert default category
    INSERT INTO category (category_name)
    VALUES ('General');
    
    -- Insert default fields for products
    INSERT INTO field_definition (entity_type, field_name, display_name, field_type, field_order, required, enabled)
    VALUES 
        ('product', 'serial_number', 'Serial Number', 'text', 1, false, true),
        ('product', 'width', 'Width', 'number', 2, false, true),
        ('product', 'length', 'Length', 'number', 3, false, true),
        ('product', 'height', 'Height', 'number', 4, false, true),
        ('product', 'weight', 'Weight', 'number', 5, false, true),
        ('product', 'color', 'Color', 'text', 6, false, false),
        ('product', 'material', 'Material', 'text', 7, false, false);
    
    -- Insert default fields for customers
    INSERT INTO field_definition (entity_type, field_name, display_name, field_type, field_order, required, enabled)
    VALUES 
        ('customer', 'website', 'Website', 'text', 1, false, false),
        ('customer', 'notes', 'Notes', 'text', 2, false, false);
    """)


def downgrade() -> None:
    # Drop all tables in reverse order
    op.drop_table('field_definition_history')
    op.drop_table('field_data')
    op.drop_table('field_definition')
    op.drop_table('bill_item')
    op.drop_table('bill')
    op.drop_table('product')
    op.drop_table('category')
    op.drop_table('customer')
    op.drop_table('company_config')
    op.drop_table('users')
