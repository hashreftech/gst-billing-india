"""
This script helps migrate the field utils functionality from using the FieldData table
to using the custom_fields JSON column in each model.

Steps:
1. Check if there's any data in the FieldData table that needs to be migrated
2. Call the migration function to copy data from FieldData to custom_fields
3. Switch the implementation by copying field_utils_json.py to field_utils.py
"""

import os
import shutil
import sys
from extensions import db
from models import FieldData

def main():
    """
    Main function to execute the migration.
    """
    # Check if there's any data in the FieldData table
    field_data_count = FieldData.query.count()
    
    if field_data_count > 0:
        print(f"Found {field_data_count} records in FieldData table that need to be migrated.")
        print("Migrating data from FieldData to custom_fields JSON columns...")
        
        # Import the migration function from field_utils_json.py
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from field_utils_json import migrate_field_data_to_json
        
        # Run the migration
        success = migrate_field_data_to_json()
        
        if success:
            print("Data migration completed successfully!")
        else:
            print("Data migration failed. Please check the logs for details.")
            return False
    else:
        print("No data found in FieldData table. Skipping data migration.")
    
    # Switch the implementation by copying field_utils_json.py to field_utils.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    field_utils_json_path = os.path.join(current_dir, 'field_utils_json.py')
    field_utils_path = os.path.join(current_dir, 'field_utils.py')
    field_utils_backup_path = os.path.join(current_dir, 'field_utils_old.py')
    
    # Backup the old field_utils.py
    shutil.copy2(field_utils_path, field_utils_backup_path)
    print(f"Backed up old field_utils.py to {field_utils_backup_path}")
    
    # Copy the new implementation
    shutil.copy2(field_utils_json_path, field_utils_path)
    print(f"Copied new implementation from {field_utils_json_path} to {field_utils_path}")
    
    print("Migration completed successfully!")
    return True

if __name__ == "__main__":
    from app import app
    with app.app_context():
        main()
