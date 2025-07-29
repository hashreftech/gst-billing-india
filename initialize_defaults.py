#!/usr/bin/env python
"""
Initialize database with default data after reset.
This script:
1. Creates a default admin user (admin/admin123)
2. Creates a sample customer
3. Creates a sample product
"""

from app import app, db
from models import User, Customer, Product, Category
from werkzeug.security import generate_password_hash
import datetime
from sqlalchemy import text

def create_admin_user():
    """Create the default admin user if it doesn't exist"""
    with app.app_context():
        # Check if admin user already exists
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print("Admin user already exists, skipping creation")
            return
        
        # Create admin user
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            email='admin@example.com',
            role='admin',
            active=True,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
        db.session.add(admin)
        db.session.commit()
        print("Default admin user created: admin/admin123")

def create_sample_customer():
    """Create a sample customer if none exist"""
    with app.app_context():
        # Check if any customers exist
        customer_count = Customer.query.count()
        if customer_count > 0:
            print("Customers already exist, skipping sample customer creation")
            return
        
        # Create a sample customer
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
        print("Sample customer created: Sample Business Pvt Ltd")

def create_sample_product():
    """Create a sample product if none exist"""
    with app.app_context():
        # Check if any products exist
        product_count = Product.query.count()
        if product_count > 0:
            print("Products already exist, skipping sample product creation")
            return
        
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
        print("Sample product created: Sample Product (₹1000, 18% GST)")

if __name__ == "__main__":
    print("Initializing database with default data...")
    create_admin_user()
    create_sample_customer()
    create_sample_product()
    print("Database initialization completed successfully!")
