"""
Migration: Initial Schema Setup
Created: 20250728120000
"""

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database URI from environment
db_uri = os.environ.get("DATABASE_URL")

def upgrade():
    """Apply the migration."""
    engine = create_engine(db_uri)
    
    with engine.connect() as conn:
        conn.execute(text('''
        -- Migration: Initial Schema Setup
        
        -- Create users table
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(80) NOT NULL UNIQUE,
            email VARCHAR(120) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            phone VARCHAR(15),
            role VARCHAR(20) NOT NULL DEFAULT 'user',
            is_active BOOLEAN NOT NULL DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create company_config table
        CREATE TABLE IF NOT EXISTS company_config (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            address TEXT NOT NULL,
            gst_number VARCHAR(15) NOT NULL,
            tan_number VARCHAR(10),
            state_code VARCHAR(2) NOT NULL,
            logo_path VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create customer table
        CREATE TABLE IF NOT EXISTS customer (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            email VARCHAR(120),
            phone VARCHAR(15),
            address TEXT,
            gst_number VARCHAR(15),
            state_code VARCHAR(2),
            is_guest BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create category table
        CREATE TABLE IF NOT EXISTS category (
            id SERIAL PRIMARY KEY,
            category_name VARCHAR(100) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create product table
        CREATE TABLE IF NOT EXISTS product (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            description TEXT,
            price NUMERIC(15, 2) NOT NULL,
            hsn_code VARCHAR(10) NOT NULL,
            gst_rate NUMERIC(5, 2) NOT NULL DEFAULT 18.0,
            unit VARCHAR(20) NOT NULL DEFAULT 'Nos',
            category_id INTEGER REFERENCES category(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create bill table
        CREATE TABLE IF NOT EXISTS bill (
            id SERIAL PRIMARY KEY,
            bill_number VARCHAR(20) NOT NULL UNIQUE,
            bill_date DATE NOT NULL,
            customer_id INTEGER REFERENCES customer(id),
            total_amount NUMERIC(15, 2) NOT NULL,
            gst_amount NUMERIC(15, 2) NOT NULL,
            discount_amount NUMERIC(15, 2) DEFAULT 0,
            final_amount NUMERIC(15, 2) NOT NULL,
            status VARCHAR(20) NOT NULL DEFAULT 'draft',
            notes TEXT,
            created_by INTEGER REFERENCES users(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create bill_item table
        CREATE TABLE IF NOT EXISTS bill_item (
            id SERIAL PRIMARY KEY,
            bill_id INTEGER NOT NULL REFERENCES bill(id) ON DELETE CASCADE,
            product_id INTEGER REFERENCES product(id),
            product_name VARCHAR(200) NOT NULL,
            quantity NUMERIC(15, 3) NOT NULL,
            unit_price NUMERIC(15, 2) NOT NULL,
            hsn_code VARCHAR(10) NOT NULL,
            gst_rate NUMERIC(5, 2) NOT NULL,
            discount_percent NUMERIC(5, 2) DEFAULT 0,
            discount_amount NUMERIC(15, 2) DEFAULT 0,
            taxable_amount NUMERIC(15, 2) NOT NULL,
            gst_amount NUMERIC(15, 2) NOT NULL,
            total_amount NUMERIC(15, 2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create field_definition table
        CREATE TABLE IF NOT EXISTS field_definition (
            id SERIAL PRIMARY KEY,
            entity_type VARCHAR(50) NOT NULL,
            field_name VARCHAR(50) NOT NULL,
            display_name VARCHAR(100) NOT NULL,
            field_type VARCHAR(20) NOT NULL,
            required BOOLEAN DEFAULT FALSE,
            enabled BOOLEAN DEFAULT TRUE,
            field_order INTEGER DEFAULT 0,
            options TEXT,
            default_value TEXT,
            validation_regex TEXT,
            help_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT uix_field_entity_name UNIQUE (entity_type, field_name)
        );
        
        -- Create field_data table
        CREATE TABLE IF NOT EXISTS field_data (
            id SERIAL PRIMARY KEY,
            field_definition_id INTEGER NOT NULL REFERENCES field_definition(id) ON DELETE CASCADE,
            entity_id INTEGER NOT NULL,
            value_text TEXT,
            value_number NUMERIC(15, 5),
            value_date TIMESTAMP,
            value_boolean BOOLEAN,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT uix_field_entity UNIQUE (field_definition_id, entity_id)
        );
        
        -- Create field_definition_history table
        CREATE TABLE IF NOT EXISTS field_definition_history (
            id SERIAL PRIMARY KEY,
            field_definition_id INTEGER NOT NULL REFERENCES field_definition(id) ON DELETE CASCADE,
            change_type VARCHAR(20) NOT NULL,
            changed_by INTEGER REFERENCES users(id),
            old_values JSONB,
            new_values JSONB,
            changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Insert default category if it doesn't exist
        INSERT INTO category (category_name)
        VALUES ('General')
        ON CONFLICT (category_name) DO NOTHING;
        
        -- Insert default fields for products
        INSERT INTO field_definition (entity_type, field_name, display_name, field_type, field_order, required, enabled)
        VALUES 
            ('product', 'serial_number', 'Serial Number', 'text', 1, FALSE, TRUE),
            ('product', 'width', 'Width', 'number', 2, FALSE, TRUE),
            ('product', 'length', 'Length', 'number', 3, FALSE, TRUE),
            ('product', 'height', 'Height', 'number', 4, FALSE, TRUE),
            ('product', 'weight', 'Weight', 'number', 5, FALSE, TRUE),
            ('product', 'color', 'Color', 'text', 6, FALSE, FALSE),
            ('product', 'material', 'Material', 'text', 7, FALSE, FALSE)
        ON CONFLICT (entity_type, field_name) DO NOTHING;
        
        -- Insert default fields for customers
        INSERT INTO field_definition (entity_type, field_name, display_name, field_type, field_order, required, enabled)
        VALUES 
            ('customer', 'website', 'Website', 'text', 1, FALSE, FALSE),
            ('customer', 'notes', 'Notes', 'text', 2, FALSE, FALSE)
        ON CONFLICT (entity_type, field_name) DO NOTHING;
        '''))
        conn.commit()

def downgrade():
    """Revert the migration."""
    engine = create_engine(db_uri)
    
    with engine.connect() as conn:
        conn.execute(text('''
        -- Downgrade: Drop all tables
        
        DROP TABLE IF EXISTS field_definition_history;
        DROP TABLE IF EXISTS field_data;
        DROP TABLE IF EXISTS field_definition;
        DROP TABLE IF EXISTS bill_item;
        DROP TABLE IF EXISTS bill;
        DROP TABLE IF EXISTS product;
        DROP TABLE IF EXISTS category;
        DROP TABLE IF EXISTS customer;
        DROP TABLE IF EXISTS company_config;
        DROP TABLE IF EXISTS users;
        '''))
        conn.commit()

if __name__ == '__main__':
    # Execute the migration functions based on command line arguments
    upgrade()
