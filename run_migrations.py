#!/usr/bin/env python
"""
Script to run all migrations in order for a fresh installation.
"""

import os
import sys
import importlib.util
from pathlib import Path

def import_module_from_file(file_path):
    """Import a module from a file path."""
    spec = importlib.util.spec_from_file_location("migration_module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def run_migrations():
    """Run all migrations in the migrations directory in order."""
    migrations_dir = Path("migrations")
    
    if not migrations_dir.exists():
        print("Migrations directory not found!")
        return False
    
    # Get all Python files in the migrations directory
    migration_files = sorted([
        f for f in migrations_dir.glob("*.py") 
        if f.is_file() and not f.name.startswith("__")
    ])
    
    if not migration_files:
        print("No migration files found!")
        return False
    
    print(f"Found {len(migration_files)} migration files:")
    for i, migration_file in enumerate(migration_files, 1):
        print(f"{i}. {migration_file.name}")
    
    print("\nRunning migrations in order...")
    
    for i, migration_file in enumerate(migration_files, 1):
        print(f"\n[{i}/{len(migration_files)}] Running migration: {migration_file.name}")
        
        try:
            # Import the migration module
            migration_module = import_module_from_file(migration_file)
            
            # Run the upgrade function
            if hasattr(migration_module, 'upgrade'):
                migration_module.upgrade()
                print(f"✓ Successfully applied migration: {migration_file.name}")
            else:
                print(f"✗ Error: Migration file {migration_file.name} has no upgrade() function!")
                return False
                
        except Exception as e:
            print(f"✗ Error applying migration {migration_file.name}:")
            print(f"  {str(e)}")
            return False
    
    print("\n✓ All migrations completed successfully!")
    return True

if __name__ == "__main__":
    success = run_migrations()
    sys.exit(0 if success else 1)
