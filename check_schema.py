#!/usr/bin/env python
"""
A simple script to check the database schema
"""
from app import app, db
from sqlalchemy import text

def check_schema():
    with app.app_context():
        # Check product table
        result = db.session.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'product' ORDER BY ordinal_position"))
        product_columns = [row[0] for row in result]
        print("Product columns:", product_columns)
        
        # Check bill_item table
        result = db.session.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'bill_item' ORDER BY ordinal_position"))
        bill_item_columns = [row[0] for row in result]
        print("BillItem columns:", bill_item_columns)
        
        # Check for cgst_rate and sgst_rate in product
        has_cgst_sgst_product = 'cgst_rate' in product_columns and 'sgst_rate' in product_columns
        print(f"Product has cgst_rate and sgst_rate columns: {has_cgst_sgst_product}")
        
        # Check for cgst_rate and sgst_rate in bill_item
        has_cgst_sgst_bill_item = 'cgst_rate' in bill_item_columns and 'sgst_rate' in bill_item_columns
        print(f"BillItem has cgst_rate and sgst_rate columns: {has_cgst_sgst_bill_item}")

if __name__ == "__main__":
    check_schema()
