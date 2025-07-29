#!/usr/bin/env python
"""
Direct database migration script for PostgreSQL.
Use this if the run_migration.py script has import issues.
"""

import os
import sys
import importlib.util

# Try to import psycopg2
try:
    import psycopg2
except ImportError:
    print("Error: psycopg2 module not found. Installing...")
    os.system("pip install psycopg2-binary")
    try:
        import psycopg2
    except ImportError:
        print("Failed to install psycopg2. Please install it manually with:")
        print("pip install psycopg2-binary")
        sys.exit(1)

# Try to import dotenv
try:
    from dotenv import load_dotenv
    # Try to load environment variables from .env file
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not found. Using environment variables directly.")

# Get DATABASE_URL from environment
database_url = os.environ.get('DATABASE_URL')

# If not found, try to create it from app.py if possible
if not database_url:
    print("DATABASE_URL not found in environment. Checking app configuration...")
    try:
        # Add the project root to the path so we can import the app
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from app import app
        with app.app_context():
            database_url = app.config.get('SQLALCHEMY_DATABASE_URI')
            print(f"Found database URL in app config: {database_url}")
    except ImportError:
        print("Warning: Could not import app to get database URL.")
    except Exception as e:
        print(f"Error accessing app config: {e}")

# If still not found, use a default value from the previous migration script
if not database_url:
    database_url = 'postgresql://postgres:postgres@localhost:5432/softwareindia'
    print(f"Using default database URL: {database_url}")

# Parse DATABASE_URL into connection parameters
try:
    # Basic parsing of postgresql://user:password@host:port/dbname
    if database_url.startswith('postgresql://'):
        # Remove postgresql://
        url = database_url[13:]
        # Split user:password@host:port/dbname
        auth_host, dbname = url.split('/', 1)
        # Split user:password@host:port
        auth, host_port = auth_host.split('@', 1)
        # Split user:password
        if ':' in auth:
            user, password = auth.split(':', 1)
        else:
            user, password = auth, ''
        # Split host:port
        if ':' in host_port:
            host, port = host_port.split(':', 1)
        else:
            host, port = host_port, '5432'
        
        # Database connection parameters
        db_params = {
            'dbname': dbname,
            'user': user,
            'password': password,
            'host': host,
            'port': port
        }
    else:
        print(f"Warning: Unrecognized database URL format: {database_url}")
        # Fallback to default parameters
        db_params = {
            'dbname': 'softwareindia',
            'user': 'postgres',
            'password': 'postgres',
            'host': 'localhost',
            'port': '5432'
        }
except Exception as e:
    print(f"Error parsing database URL: {e}")
    # Fallback to default parameters
    db_params = {
        'dbname': 'softwareindia',
        'user': 'postgres',
        'password': 'postgres',
        'host': 'localhost',
        'port': '5432'
    }

def run_migration():
    """Execute the SQL migration script."""
    try:
        # Connect to the database
        print("Connecting to the database with parameters:")
        # Print connection details but hide password
        safe_params = db_params.copy()
        if 'password' in safe_params:
            safe_params['password'] = '****' if safe_params['password'] else '(empty)'
        print(safe_params)
        
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        # Read the SQL script
        script_path = os.path.join(os.path.dirname(__file__), 'add_cgst_sgst_columns.sql')
        print(f"Reading SQL script from: {script_path}")
        with open(script_path, 'r') as f:
            sql_script = f.read()
        
        print("Executing migration script...")
        cursor.execute(sql_script)
        conn.commit()
        print("Migration completed successfully!")
        
        # Close connections
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Starting database migration...")
    if run_migration():
        print("Migration completed successfully.")
    else:
        print("Migration failed. Check the error messages above.")
        sys.exit(1)
