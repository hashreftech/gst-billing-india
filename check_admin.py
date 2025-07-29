#!/usr/bin/env python
"""
Script to check if admin user exists and validate login credentials.
"""

from app import app, db
from models import User
from werkzeug.security import check_password_hash

def check_admin():
    with app.app_context():
        # Check if admin user exists
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("Admin user does not exist!")
            return
        
        print(f"Admin user found with ID: {admin.id}")
        print(f"Username: {admin.username}")
        print(f"Email: {admin.email}")
        print(f"Role: {admin.role}")
        print(f"Is Active: {admin.is_active}")
        
        # Check password
        if admin.password_hash:
            print(f"Password hash exists: {admin.password_hash[:10]}...")
            test_password = 'admin123'
            is_valid = check_password_hash(admin.password_hash, test_password)
            print(f"Password 'admin123' is {'valid' if is_valid else 'INVALID'}")
        else:
            print("Password hash is empty or None!")

        # Check other admin users
        all_admins = User.query.filter_by(role='admin').all()
        print(f"Total admin users found: {len(all_admins)}")
        for i, a in enumerate(all_admins):
            print(f"Admin {i+1}: {a.username} (ID: {a.id}, Active: {a.is_active})")

if __name__ == "__main__":
    check_admin()
