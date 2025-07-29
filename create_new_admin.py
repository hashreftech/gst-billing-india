#!/usr/bin/env python
"""
Script to create a new admin user with the correct password hashing.
"""

from app import app, db
from models import User
from werkzeug.security import generate_password_hash
import datetime

def create_admin():
    with app.app_context():
        # Check if there are any users
        user_count = User.query.count()
        print(f"Total users in database: {user_count}")
        
        # Find existing admin users
        admin_users = User.query.filter_by(username='admin').all()
        if admin_users:
            print(f"Found {len(admin_users)} admin users with username 'admin'")
            # Delete them
            for admin in admin_users:
                print(f"Deleting admin user with ID {admin.id}")
                db.session.delete(admin)
            db.session.commit()
            print("Deleted existing admin users")
        
        # Create new admin user
        admin = User(
            username='admin',
            email='admin@example.com',
            role='admin',
            is_active=True,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now()
        )
        
        # Set password properly using the model's method
        admin.set_password('admin123')
        
        # Save to database
        db.session.add(admin)
        db.session.commit()
        
        print(f"Created new admin user with ID: {admin.id}")
        print(f"Username: {admin.username}")
        print(f"Password: admin123")
        print(f"Password hash: {admin.password_hash[:15]}...")

if __name__ == "__main__":
    create_admin()
