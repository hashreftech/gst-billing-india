
"""
Migration: enable_product_fields
Created: 20250728112541
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
        -- Migration: Enable default product fields
        
        -- Ensure the field_definition table exists
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
        
        -- Enable serial_number field if it exists
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM field_definition 
                      WHERE entity_type='product' AND field_name='serial_number') THEN
                UPDATE field_definition 
                SET enabled = TRUE, 
                    display_name = 'Serial Number',
                    field_type = 'text',
                    help_text = 'Enter the product serial number or SKU'
                WHERE entity_type='product' AND field_name='serial_number';
            ELSE
                INSERT INTO field_definition 
                (entity_type, field_name, display_name, field_type, required, enabled, field_order, help_text)
                VALUES 
                ('product', 'serial_number', 'Serial Number', 'text', FALSE, TRUE, 1, 'Enter the product serial number or SKU');
            END IF;
        END $$;
        
        -- Enable width field if it exists
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM field_definition 
                      WHERE entity_type='product' AND field_name='width') THEN
                UPDATE field_definition 
                SET enabled = TRUE, 
                    display_name = 'Width (cm)',
                    field_type = 'number',
                    help_text = 'Product width in centimeters'
                WHERE entity_type='product' AND field_name='width';
            ELSE
                INSERT INTO field_definition 
                (entity_type, field_name, display_name, field_type, required, enabled, field_order, help_text)
                VALUES 
                ('product', 'width', 'Width (cm)', 'number', FALSE, TRUE, 2, 'Product width in centimeters');
            END IF;
        END $$;
        
        -- Enable length field if it exists
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM field_definition 
                      WHERE entity_type='product' AND field_name='length') THEN
                UPDATE field_definition 
                SET enabled = TRUE, 
                    display_name = 'Length (cm)',
                    field_type = 'number',
                    help_text = 'Product length in centimeters'
                WHERE entity_type='product' AND field_name='length';
            ELSE
                INSERT INTO field_definition 
                (entity_type, field_name, display_name, field_type, required, enabled, field_order, help_text)
                VALUES 
                ('product', 'length', 'Length (cm)', 'number', FALSE, TRUE, 3, 'Product length in centimeters');
            END IF;
        END $$;
        '''))
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
        -- Downgrade: Disable product fields
        
        -- Disable serial_number field
        UPDATE field_definition 
        SET enabled = FALSE
        WHERE entity_type='product' AND field_name='serial_number';
        
        -- Disable width field
        UPDATE field_definition 
        SET enabled = FALSE
        WHERE entity_type='product' AND field_name='width';
        
        -- Disable length field
        UPDATE field_definition 
        SET enabled = FALSE
        WHERE entity_type='product' AND field_name='length';
        '''))
        conn.commit()

if __name__ == '__main__':
    # Execute the migration functions based on command line arguments
    upgrade()
        