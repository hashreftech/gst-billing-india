#!/usr/bin/env python
"""
Migration runner script to apply database migrations.
This script is designed to be run from the command line.
"""

import os
import sys
import importlib.util
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Verify database connection URL is set
if not os.environ.get("DATABASE_URL"):
    print("Error: DATABASE_URL environment variable is not set.")
    print("Please set it in your .env file or environment.")
    sys.exit(1)

def list_migrations():
    """List all available migrations in the migrations directory."""
    if not os.path.exists("migrations"):
        print("No migrations directory found.")
        return []
    
    migrations = []
    for file in os.listdir("migrations"):
        if file.endswith(".py") and not file.startswith("__"):
            migrations.append(file)
    
    return sorted(migrations)

def run_migration(migration_file):
    """Run a specific migration file."""
    full_path = os.path.join("migrations", migration_file)
    
    if not os.path.exists(full_path):
        print(f"Error: Migration file {full_path} not found.")
        return False
    
    print(f"Applying migration: {migration_file}")
    
    # Import the migration module dynamically
    spec = importlib.util.spec_from_file_location(
        migration_file.replace(".py", ""), 
        full_path
    )
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)
    
    # Run the upgrade function
    try:
        migration.upgrade()
        print(f"Migration {migration_file} applied successfully!")
        return True
    except Exception as e:
        print(f"Error applying migration {migration_file}: {str(e)}")
        return False

def print_help():
    """Print help message for the script."""
    print("Database Migration Runner")
    print("========================")
    print()
    print("Usage:")
    print("  ./migrate.py list                 - List all available migrations")
    print("  ./migrate.py apply [filename]     - Apply a specific migration")
    print("  ./migrate.py apply-all            - Apply all pending migrations")
    print("  ./migrate.py help                 - Show this help message")
    print()

if __name__ == "__main__":
    # Make the script executable
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "list":
        migrations = list_migrations()
        if migrations:
            print("Available migrations:")
            for migration in migrations:
                print(f"  {migration}")
        else:
            print("No migrations found.")
    
    elif command == "apply" and len(sys.argv) > 2:
        migration_file = sys.argv[2]
        if not migration_file.endswith(".py"):
            migration_file += ".py"
        success = run_migration(migration_file)
        sys.exit(0 if success else 1)
    
    elif command == "apply-all":
        migrations = list_migrations()
        if not migrations:
            print("No migrations found.")
            sys.exit(0)
        
        success = True
        for migration in migrations:
            if not run_migration(migration):
                success = False
                break
        
        if success:
            print("All migrations applied successfully!")
        sys.exit(0 if success else 1)
    
    elif command == "help":
        print_help()
    
    else:
        print(f"Unknown command: {command}")
        print_help()
        sys.exit(1)
