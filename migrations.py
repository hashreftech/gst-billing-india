"""
This module sets up database migrations using Alembic directly.
It provides a standardized way to evolve the database schema as the application grows.
"""

from app import app, db
import models  # Import all models to ensure they're detected
import os
import sys

def create_migration(migration_name):
    """Create a new migration file with the specified name."""
    if not os.path.exists("migrations"):
        os.makedirs("migrations")
    
    timestamp = os.popen('date +%Y%m%d%H%M%S').read().strip()
    migration_file = f"migrations/{timestamp}_{migration_name}.py"
    
    with open(migration_file, "w") as f:
        f.write("""
\"\"\"
Migration: {migration_name}
Created: {timestamp}
\"\"\"

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database URI from environment
db_uri = os.environ.get("DATABASE_URL")

def upgrade():
    \"\"\"Apply the migration.\"\"\"
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
    \"\"\"Revert the migration.\"\"\"
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

if __name__ == '__main__':
    # Execute the migration functions based on command line arguments
    upgrade()
        """.format(
            migration_name=migration_name,
            timestamp=timestamp
        ))
    
    print(f"Created migration file: {migration_file}")
    return migration_file

def apply_migration(migration_file):
    """Apply the specified migration."""
    if not os.path.exists(migration_file):
        print(f"Migration file not found: {migration_file}")
        return False
    
    # Execute the migration file
    migration_dir = os.path.dirname(migration_file)
    sys.path.append(migration_dir)
    
    # Extract the filename without extension
    migration_module = os.path.basename(migration_file).replace('.py', '')
    
    # Import the module and execute upgrade()
    migration = __import__(migration_module)
    migration.upgrade()
    
    print(f"Applied migration: {migration_file}")
    return True

def list_migrations():
    """List all available migrations."""
    if not os.path.exists("migrations"):
        print("No migrations directory found.")
        return []
    
    migrations = []
    for file in os.listdir("migrations"):
        if file.endswith(".py") and not file.startswith("__"):
            migrations.append(os.path.join("migrations", file))
    
    return sorted(migrations)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database migration utility")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Create migration command
    create_parser = subparsers.add_parser("create", help="Create a new migration")
    create_parser.add_argument("name", help="Name of the migration")
    
    # Apply migration command
    apply_parser = subparsers.add_parser("apply", help="Apply a migration")
    apply_parser.add_argument("file", nargs="?", help="Migration file to apply (default: latest)")
    
    # List migrations command
    list_parser = subparsers.add_parser("list", help="List all migrations")
    
    args = parser.parse_args()
    
    if args.command == "create":
        create_migration(args.name)
    elif args.command == "apply":
        migrations = list_migrations()
        if not migrations:
            print("No migrations found.")
        elif args.file:
            apply_migration(args.file)
        elif migrations:
            apply_migration(migrations[-1])  # Apply the latest migration
        else:
            print("No migration file specified.")
    elif args.command == "list":
        migrations = list_migrations()
        if migrations:
            print("Available migrations:")
            for migration in migrations:
                print(f"  {migration}")
        else:
            print("No migrations found.")
    else:
        parser.print_help()
