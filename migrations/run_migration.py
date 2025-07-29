#!/usr/bin/env python
"""
Execute SQL migration script using the app's database connection.
This is a safer way to run migrations as it uses the existing app configuration.
"""

import os
import sys
from pathlib import Path

# Add the project root directory to the path so we can import the app
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

try:
    # Import the app and db from the main application
    from app import app, db
    
    # Setup the application context
    with app.app_context():
        # Read the SQL script
        sql_file_path = os.path.join(current_dir, 'add_cgst_sgst_columns.sql')
        with open(sql_file_path, 'r') as f:
            sql_script = f.read()
        
        print("Executing migration script...")
        # Execute the SQL directly using the db connection
        db.session.execute(sql_script)
        db.session.commit()
        print("Migration completed successfully!")

except ImportError as e:
    print(f"Error importing application: {e}")
    print("Make sure you're running this script from the project root directory.")
    sys.exit(1)
except Exception as e:
    print(f"Error executing migration: {e}")
    sys.exit(1)
