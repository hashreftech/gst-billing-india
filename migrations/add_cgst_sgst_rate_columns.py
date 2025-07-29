"""
Add CGST and SGST rate columns to Product and BillItem tables

This migration script adds the cgst_rate and sgst_rate columns to the Product and BillItem tables,
defaulting to half of the existing gst_rate value.
"""

import os
import sys

# Add the parent directory to the path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extensions import db
from app import create_app

def run_migration():
    """Run the migration to add cgst_rate and sgst_rate columns"""
    app = create_app()
    
    with app.app_context():
        # Check if columns already exist
        conn = db.engine.connect()
        
        # Check if product table has the new columns
        product_cols = conn.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='product' AND column_name IN ('cgst_rate', 'sgst_rate')
        """).fetchall()
        
        product_needs_migration = len(product_cols) < 2
        
        # Check if bill_item table has the new columns
        bill_item_cols = conn.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='bill_item' AND column_name IN ('cgst_rate', 'sgst_rate')
        """).fetchall()
        
        bill_item_needs_migration = len(bill_item_cols) < 2
        
        if product_needs_migration:
            print("Adding cgst_rate and sgst_rate columns to product table...")
            # Add columns to product table if they don't exist
            conn.execute("""
                ALTER TABLE product 
                ADD COLUMN IF NOT EXISTS cgst_rate NUMERIC(5,2) NOT NULL DEFAULT 9.0,
                ADD COLUMN IF NOT EXISTS sgst_rate NUMERIC(5,2) NOT NULL DEFAULT 9.0
            """)
            
            # Update the values of cgst_rate and sgst_rate based on gst_rate
            conn.execute("""
                UPDATE product 
                SET cgst_rate = gst_rate / 2,
                    sgst_rate = gst_rate / 2
            """)
            print("Product table migration completed successfully.")
        else:
            print("Product table already has the required columns.")
        
        if bill_item_needs_migration:
            print("Adding cgst_rate and sgst_rate columns to bill_item table...")
            # Add columns to bill_item table if they don't exist
            conn.execute("""
                ALTER TABLE bill_item 
                ADD COLUMN IF NOT EXISTS cgst_rate NUMERIC(5,2) NOT NULL DEFAULT 0,
                ADD COLUMN IF NOT EXISTS sgst_rate NUMERIC(5,2) NOT NULL DEFAULT 0
            """)
            
            # Update the values of cgst_rate and sgst_rate based on gst_rate
            conn.execute("""
                UPDATE bill_item 
                SET cgst_rate = gst_rate / 2,
                    sgst_rate = gst_rate / 2
            """)
            print("BillItem table migration completed successfully.")
        else:
            print("BillItem table already has the required columns.")
        
        conn.close()
        
        print("Migration completed successfully!")

if __name__ == "__main__":
    run_migration()
