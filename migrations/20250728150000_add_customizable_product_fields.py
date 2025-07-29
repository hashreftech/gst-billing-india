"""
Migration: add_customizable_product_fields
Created: 20250728150000
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
        # Create field definitions table to store metadata about custom fields
        conn.execute(text('''
        -- Create custom field definitions table
        CREATE TABLE IF NOT EXISTS field_definition (
            id SERIAL PRIMARY KEY,
            entity_type VARCHAR(50) NOT NULL,  -- 'product', 'customer', etc.
            field_name VARCHAR(50) NOT NULL,
            display_name VARCHAR(100) NOT NULL,
            field_type VARCHAR(20) NOT NULL,   -- 'text', 'number', 'date', 'boolean', 'select'
            required BOOLEAN DEFAULT FALSE,
            enabled BOOLEAN DEFAULT TRUE,
            field_order INTEGER DEFAULT 0,
            options TEXT,                      -- JSON string for select options
            default_value TEXT,
            validation_regex TEXT,
            help_text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (entity_type, field_name)
        );
        
        -- Create table to store the actual field values
        CREATE TABLE IF NOT EXISTS field_data (
            id SERIAL PRIMARY KEY,
            field_definition_id INTEGER NOT NULL REFERENCES field_definition(id) ON DELETE CASCADE,
            entity_id INTEGER NOT NULL,       -- ID of the product, customer, etc.
            value_text TEXT,
            value_number NUMERIC(15,5),
            value_date TIMESTAMP,
            value_boolean BOOLEAN,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (field_definition_id, entity_id)
        );
        
        -- Create index for faster field lookups
        CREATE INDEX IF NOT EXISTS idx_field_data_entity_id ON field_data (entity_id);
        
        -- Insert sample field definitions for products
        INSERT INTO field_definition (
            entity_type, field_name, display_name, field_type, 
            required, enabled, field_order, default_value
        )
        VALUES 
            ('product', 'serial_number', 'Serial Number', 'text', FALSE, TRUE, 1, NULL),
            ('product', 'width', 'Width', 'number', FALSE, TRUE, 2, NULL),
            ('product', 'length', 'Length', 'number', FALSE, TRUE, 3, NULL),
            ('product', 'height', 'Height', 'number', FALSE, TRUE, 4, NULL),
            ('product', 'weight', 'Weight', 'number', FALSE, TRUE, 5, NULL),
            ('product', 'color', 'Color', 'text', FALSE, FALSE, 6, NULL),
            ('product', 'material', 'Material', 'text', FALSE, FALSE, 7, NULL)
        ON CONFLICT (entity_type, field_name) DO NOTHING;
        '''))
        conn.commit()
        
        # Add history table for field changes
        conn.execute(text('''
        -- Create field_definition_history table to track changes
        CREATE TABLE IF NOT EXISTS field_definition_history (
            id SERIAL PRIMARY KEY,
            field_definition_id INTEGER NOT NULL REFERENCES field_definition(id) ON DELETE CASCADE,
            change_type VARCHAR(20) NOT NULL,  -- 'create', 'update', 'delete'
            changed_by INTEGER,               -- User ID who made the change
            old_values JSONB,                 -- Previous values in JSON format
            new_values JSONB,                 -- New values in JSON format
            changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create function and trigger to log field definition changes
        CREATE OR REPLACE FUNCTION log_field_definition_change()
        RETURNS TRIGGER AS $$
        BEGIN
            IF TG_OP = 'INSERT' THEN
                INSERT INTO field_definition_history (
                    field_definition_id, change_type, old_values, new_values
                ) VALUES (
                    NEW.id, 'create', NULL, 
                    jsonb_build_object(
                        'entity_type', NEW.entity_type,
                        'field_name', NEW.field_name,
                        'display_name', NEW.display_name,
                        'field_type', NEW.field_type,
                        'required', NEW.required,
                        'enabled', NEW.enabled
                    )
                );
            ELSIF TG_OP = 'UPDATE' THEN
                INSERT INTO field_definition_history (
                    field_definition_id, change_type, old_values, new_values
                ) VALUES (
                    NEW.id, 'update', 
                    jsonb_build_object(
                        'entity_type', OLD.entity_type,
                        'field_name', OLD.field_name,
                        'display_name', OLD.display_name,
                        'field_type', OLD.field_type,
                        'required', OLD.required,
                        'enabled', OLD.enabled
                    ),
                    jsonb_build_object(
                        'entity_type', NEW.entity_type,
                        'field_name', NEW.field_name,
                        'display_name', NEW.display_name,
                        'field_type', NEW.field_type,
                        'required', NEW.required,
                        'enabled', NEW.enabled
                    )
                );
            ELSIF TG_OP = 'DELETE' THEN
                INSERT INTO field_definition_history (
                    field_definition_id, change_type, old_values, new_values
                ) VALUES (
                    OLD.id, 'delete', 
                    jsonb_build_object(
                        'entity_type', OLD.entity_type,
                        'field_name', OLD.field_name,
                        'display_name', OLD.display_name,
                        'field_type', OLD.field_type,
                        'required', OLD.required,
                        'enabled', OLD.enabled
                    ),
                    NULL
                );
            END IF;
            RETURN NULL;
        END;
        $$ LANGUAGE plpgsql;
        
        -- Only create trigger if it doesn't exist
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_trigger 
                WHERE tgname = 'trigger_field_definition_history'
            ) THEN
                CREATE TRIGGER trigger_field_definition_history
                AFTER INSERT OR UPDATE OR DELETE ON field_definition
                FOR EACH ROW EXECUTE FUNCTION log_field_definition_change();
            END IF;
        END $$;
        '''))
        conn.commit()

def downgrade():
    """Revert the migration."""
    engine = create_engine(db_uri)
    
    with engine.connect() as conn:
        conn.execute(text('''
        -- Drop trigger if exists
        DROP TRIGGER IF EXISTS trigger_field_definition_history ON field_definition;
        
        -- Drop function if exists
        DROP FUNCTION IF EXISTS log_field_definition_change();
        
        -- Drop tables in reverse order of dependencies
        DROP TABLE IF EXISTS field_definition_history;
        DROP TABLE IF EXISTS field_data;
        DROP TABLE IF EXISTS field_definition;
        '''))
        conn.commit()
