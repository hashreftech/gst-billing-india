#!/usr/bin/env python
"""
Database Management Script using Alembic

This script provides commands to:
1. Initialize the database schema
2. Reset the database completely
3. Upgrade to the latest migration
4. Downgrade to a specific migration
5. Create a new migration
6. Reset and initialize the database with default data

Usage:
    python db_manage.py init                     # Initialize the database with all tables
    python db_manage.py reset                    # Reset the database and recreate all tables
    python db_manage.py reset-with-data          # Reset the database and populate with default data
    python db_manage.py init-data                # Initialize database with default data only
    python db_manage.py upgrade                  # Apply all unapplied migrations
    python db_manage.py downgrade [revision]     # Downgrade to a specific revision
    python db_manage.py revision "message"       # Create a new migration
"""

import os
import sys
import argparse
import subprocess
import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError

# Load environment variables
load_dotenv()

# Get database URI
db_uri = os.environ.get("DATABASE_URL")
if not db_uri:
    print("Error: DATABASE_URL environment variable not set.")
    sys.exit(1)

def run_alembic_command(command_name, *args):
    """Run an Alembic command"""
    # Use the module directly rather than the command-line tool
    from alembic.config import Config
    from alembic import command
    
    # Get alembic.ini path
    alembic_ini = os.path.join(os.path.dirname(__file__), 'alembic.ini')
    
    # Create Alembic config
    alembic_cfg = Config(alembic_ini)
    
    try:
        # Run the appropriate command
        if command_name == "upgrade":
            command.upgrade(alembic_cfg, args[0] if args else "head")
        elif command_name == "downgrade":
            command.downgrade(alembic_cfg, args[0] if args else "-1")
        elif command_name == "revision":
            message = args[0] if args else ""
            command.revision(alembic_cfg, message=message, autogenerate=True)
        else:
            print(f"Unknown command: {command_name}")
            return False
        return True
    except Exception as e:
        print(f"Error running alembic command: {e}")
        return False

def get_db_name_from_uri(uri):
    """Extract database name from URI"""
    return uri.split("/")[-1]

def reset_database():
    """Reset the database by dropping and recreating schema objects"""
    # Instead of dropping and recreating the database, we'll drop all tables and recreate them
    engine = create_engine(db_uri)
    
    with engine.connect() as conn:
        try:
            # Drop all tables in reverse order of dependency
            conn.execute(text("DROP TABLE IF EXISTS field_definition_history CASCADE;"))
            conn.execute(text("DROP TABLE IF EXISTS field_data CASCADE;"))
            conn.execute(text("DROP TABLE IF EXISTS field_definition CASCADE;"))
            conn.execute(text("DROP TABLE IF EXISTS bill_item CASCADE;"))
            conn.execute(text("DROP TABLE IF EXISTS bill CASCADE;"))
            conn.execute(text("DROP TABLE IF EXISTS product CASCADE;"))
            conn.execute(text("DROP TABLE IF EXISTS category CASCADE;"))
            conn.execute(text("DROP TABLE IF EXISTS customer CASCADE;"))
            conn.execute(text("DROP TABLE IF EXISTS company_config CASCADE;"))
            conn.execute(text("DROP TABLE IF EXISTS users CASCADE;"))
            
            # Drop the alembic_version table
            conn.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE;"))
            
            print("All tables have been dropped successfully.")
            conn.commit()
        except Exception as e:
            print(f"Error dropping tables: {e}")
            return False
    
    # Run migrations to recreate all tables
    success = run_alembic_command("upgrade", "head")
    if success:
        print("Database schema has been reset successfully.")
    else:
        print("Failed to reset database schema.")
    
    return success

def init_database():
    """Initialize the database with all tables"""
    
    # Check if database exists and tables are present
    try:
        engine = create_engine(db_uri)
        with engine.connect() as conn:
            # Check if alembic_version table exists
            result = conn.execute(text(
                "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'alembic_version')"
            ))
            table_exists = result.scalar()
            
            if table_exists:
                print("Database schema already initialized.")
                return True
    except Exception as e:
        print(f"Error checking database: {e}")
    
    # Run migrations to create all tables
    success = run_alembic_command("upgrade", "head")
    if success:
        print("Database initialized successfully with all tables.")
    else:
        print("Failed to initialize database.")
    
    return success

def upgrade_database():
    """Upgrade the database to the latest migration"""
    success = run_alembic_command("upgrade", "head")
    if success:
        print("Database upgraded successfully to the latest version.")
    else:
        print("Failed to upgrade database.")
    
    return success

def downgrade_database(revision):
    """Downgrade the database to a specific revision"""
    target = revision if revision else "-1"
    success = run_alembic_command("downgrade", target)
    
    if success:
        print(f"Database downgraded successfully to {target}.")
    else:
        print(f"Failed to downgrade database to {target}.")
    
    return success

def create_revision(message):
    """Create a new migration revision"""
    if not message:
        print("Error: Revision message is required.")
        return False
    
    try:
        from alembic.config import Config
        from alembic import command
        
        # Get alembic.ini path
        alembic_ini = os.path.join(os.path.dirname(__file__), 'alembic.ini')
        
        # Create Alembic config
        alembic_cfg = Config(alembic_ini)
        
        # Create a revision without autogenerate
        command.revision(alembic_cfg, message=message, autogenerate=False)
        print(f"Created new migration with message: '{message}'")
        return True
    except Exception as e:
        print(f"Error creating migration: {e}")
        return False

def initialize_data():
    """Initialize database with default data (admin user, sample customer, and product)"""
    try:
        print("Initializing database with default data...")
        
        # Import the required modules and models
        from app import app, db
        from models import User, Customer, Product, Category, Company
        from werkzeug.security import generate_password_hash
        
        with app.app_context():
            # Dispose of the engine's connection pool.
            # This is critical to ensure the session gets a fresh connection
            # and sees the empty database after a reset.
            print("Disposing database engine connection pool to ensure a fresh start.")
            db.engine.dispose()

            # Create admin user if it doesn't exist
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                # Explicitly create the password hash
                hashed_password = generate_password_hash('admin123')
                
                admin = User(
                    username='admin',
                    email='admin@example.com',
                    password_hash=hashed_password,  # Pass the hash directly
                    role='admin',
                    is_active=True, 
                    created_at=datetime.datetime.now(),
                    updated_at=datetime.datetime.now()
                )
                db.session.add(admin)
                db.session.commit()
                print("Created default admin user (username: admin, password: admin123)")
            else:
                print("Admin user already exists, skipping creation")
            
            # Create sample company if none exist
            company_count = Company.query.count()
            if company_count == 0:
                sample_company = Company(
                    name="My Awesome Company",
                    address="456 Business Avenue, Bangalore, Karnataka",
                    gst_number="29AABCA1234A1Z5",  # Sample GST for Karnataka
                    tan_number="BLRA12345B",
                    state_code="29",
                    created_at=datetime.datetime.now(),
                    updated_at=datetime.datetime.now()
                )
                db.session.add(sample_company)
                db.session.commit()
                print("Created sample company: My Awesome Company")
            else:
                print("Company config already exists, skipping sample company creation")

            # Create sample customer if none exist
            customer_count = Customer.query.count()
            if customer_count == 0:
                sample_customer = Customer(
                    name="Sample Business Pvt Ltd",
                    gst_number="27AABCS1234A1Z5",  # Sample GST number for Maharashtra
                    address="123 Main Street, Mumbai",
                    state_code="27",
                    phone="9876543210",
                    email="contact@samplebusiness.com",
                    created_at=datetime.datetime.now(),
                    updated_at=datetime.datetime.now()
                )
                db.session.add(sample_customer)
                db.session.commit()
                print("Created sample customer: Sample Business Pvt Ltd")
            else:
                print("Customers already exist, skipping sample customer creation")
            
            # Create sample product if none exist
            product_count = Product.query.count()
            if product_count == 0:
                # Create default category if needed
                category = Category.query.filter_by(category_name="General").first()
                if not category:
                    category = Category(
                        category_name="General",
                        created_at=datetime.datetime.now(),
                        updated_at=datetime.datetime.now()
                    )
                    db.session.add(category)
                    db.session.commit()
                    print("Created default 'General' category")
                
                # Create a sample product
                sample_product = Product(
                    name="Sample Product",
                    description="This is a sample product for demonstration",
                    price=1000.00,
                    hsn_code="8471",  # Sample HSN code for computer equipment
                    gst_rate=18.0,    # 18% GST rate
                    cgst_rate=9.0,    # 9% CGST rate
                    sgst_rate=9.0,    # 9% SGST rate
                    unit="Pcs",
                    category_id=category.id,
                    created_at=datetime.datetime.now(),
                    updated_at=datetime.datetime.now()
                )
                db.session.add(sample_product)
                db.session.commit()
                print("Created sample product: Sample Product (₹1000, 18% GST)")
            else:
                print("Products already exist, skipping sample product creation")
            
            print("Database initialization with default data completed successfully!")
            return True
    except Exception as e:
        print(f"Error initializing database with default data: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Database Management Tool")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize database with all tables")
    
    # Reset command
    reset_parser = subparsers.add_parser("reset", help="Reset database and recreate all tables")
    
    # Reset with data command
    reset_with_data_parser = subparsers.add_parser("reset-with-data", help="Reset database and populate with default data")
    
    # Init data command
    init_data_parser = subparsers.add_parser("init-data", help="Initialize database with default data only")
    
    # Upgrade command
    upgrade_parser = subparsers.add_parser("upgrade", help="Apply all unapplied migrations")
    
    # Downgrade command
    downgrade_parser = subparsers.add_parser("downgrade", help="Downgrade to a specific revision")
    downgrade_parser.add_argument("revision", nargs="?", help="Target revision (default: -1)")
    
    # Revision command
    revision_parser = subparsers.add_parser("revision", help="Create a new migration")
    revision_parser.add_argument("message", help="Migration message")
    
    args = parser.parse_args()
    
    if args.command == "init":
        init_database()
    elif args.command == "reset":
        reset_database()
    elif args.command == "reset-with-data":
        if reset_database():
            initialize_data()
    elif args.command == "init-data":
        initialize_data()
    elif args.command == "upgrade":
        upgrade_database()
    elif args.command == "downgrade":
        downgrade_database(args.revision)
    elif args.command == "revision":
        create_revision(args.message)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
