#!/usr/bin/env python
"""
Database Management Script using Alembic

This script provides commands to:
1. Initialize the database schema
2. Reset the database completely
3. Upgrade to the latest migration
4. Downgrade to a specific migration
5. Create a new migration

Usage:
    python db_manage.py init     # Initialize the database with all tables
    python db_manage.py reset    # Reset the database and recreate all tables
    python db_manage.py upgrade  # Apply all unapplied migrations
    python db_manage.py downgrade [revision]  # Downgrade to a specific revision
    python db_manage.py revision "message"    # Create a new migration
"""

import os
import sys
import argparse
import subprocess
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

def main():
    parser = argparse.ArgumentParser(description="Database Management Tool")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize database with all tables")
    
    # Reset command
    reset_parser = subparsers.add_parser("reset", help="Reset database and recreate all tables")
    
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
