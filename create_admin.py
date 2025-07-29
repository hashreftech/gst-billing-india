
from app import app, db
from models import User
from flask.cli import with_appcontext
import click

@click.command("create-admin")
@with_appcontext
def create_admin():
    """Create admin user"""
    admin = User.query.filter_by(username="admin").first()
    if admin:
        print("Admin user already exists")
        return
    
    admin = User(
        username="admin",
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        role="admin",
        is_active=True
    )
    admin.set_password("admin123")
    db.session.add(admin)
    db.session.commit()
    print("Admin user created successfully")

app.cli.add_command(create_admin)

