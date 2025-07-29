"""
Migration: add_product_fields
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
        # Write your migration SQL statements here
        conn.execute(text('''
        -- Migration: Add new fields to Product table
        
        -- Check if serial_number column exists and add if it doesn't
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                          WHERE table_name='product' AND column_name='serial_number') THEN
                ALTER TABLE product ADD COLUMN serial_number VARCHAR(50);
            END IF;
        END $$;
        
        -- Check if width column exists and add if it doesn't
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                          WHERE table_name='product' AND column_name='width') THEN
                ALTER TABLE product ADD COLUMN width NUMERIC(10, 2);
            END IF;
        END $$;
        
        -- Check if length column exists and add if it doesn't
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                          WHERE table_name='product' AND column_name='length') THEN
                ALTER TABLE product ADD COLUMN length NUMERIC(10, 2);
            END IF;
        END $$;
        
        -- Check if height column exists and add if it doesn't
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                          WHERE table_name='product' AND column_name='height') THEN
                ALTER TABLE product ADD COLUMN height NUMERIC(10, 2);
            END IF;
        END $$;
        
        -- Check if weight column exists and add if it doesn't
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                          WHERE table_name='product' AND column_name='weight') THEN
                ALTER TABLE product ADD COLUMN weight NUMERIC(10, 2);
            END IF;
        END $$;
        
        -- Create product_field_settings table if it doesn't exist
        CREATE TABLE IF NOT EXISTS product_field_settings (
            id SERIAL PRIMARY KEY,
            field_name VARCHAR(50) NOT NULL UNIQUE,
            display_name VARCHAR(100) NOT NULL,
            is_enabled BOOLEAN DEFAULT FALSE,
            field_type VARCHAR(20) DEFAULT 'text',
            field_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Insert default field settings if they don't exist
        INSERT INTO product_field_settings (field_name, display_name, field_type, field_order, is_enabled)
        VALUES 
            ('serial_number', 'Serial Number', 'text', 1, FALSE),
            ('width', 'Width', 'number', 2, FALSE),
            ('length', 'Length', 'number', 3, FALSE),
            ('height', 'Height', 'number', 4, FALSE),
            ('weight', 'Weight', 'number', 5, FALSE)
        ON CONFLICT (field_name) DO NOTHING;
        '''))
        conn.commit()

def downgrade():
    """Revert the migration."""
    engine = create_engine(db_uri)
    
    with engine.connect() as conn:
        # Write your rollback SQL statements here
        conn.execute(text('''
        -- Downgrade: Remove added columns from Product table
        
        -- Remove added columns if they exist
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM information_schema.columns 
                      WHERE table_name='product' AND column_name='serial_number') THEN
                ALTER TABLE product DROP COLUMN serial_number;
            END IF;
            
            IF EXISTS (SELECT 1 FROM information_schema.columns 
                      WHERE table_name='product' AND column_name='width') THEN
                ALTER TABLE product DROP COLUMN width;
            END IF;
            
            IF EXISTS (SELECT 1 FROM information_schema.columns 
                      WHERE table_name='product' AND column_name='length') THEN
                ALTER TABLE product DROP COLUMN length;
            END IF;
            
            IF EXISTS (SELECT 1 FROM information_schema.columns 
                      WHERE table_name='product' AND column_name='height') THEN
                ALTER TABLE product DROP COLUMN height;
            END IF;
            
            IF EXISTS (SELECT 1 FROM information_schema.columns 
                      WHERE table_name='product' AND column_name='weight') THEN
                ALTER TABLE product DROP COLUMN weight;
            END IF;
        END $$;
        
        -- Drop product_field_settings table if it exists
        DROP TABLE IF EXISTS product_field_settings;
        '''))
        conn.commit()
