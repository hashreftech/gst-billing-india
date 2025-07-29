from dotenv import load_dotenv
load_dotenv()
import os
import logging
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from extensions import db

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Configure upload folder
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure WTF CSRF protection
app.config['WTF_CSRF_TIME_LIMIT'] = None  # No time limit for CSRF tokens
app.config['WTF_CSRF_SSL_STRICT'] = False  # Allow non-HTTPS in development

# Initialize the app with the extension
db.init_app(app)

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize Flask-Login
from models import Anonymous
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'
login_manager.anonymous_user = Anonymous

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# Register template filters
from utils import number_to_words, format_currency
app.jinja_env.filters['number_to_words'] = number_to_words
app.jinja_env.filters['format_currency'] = format_currency

with app.app_context():
    # Import models to ensure tables are created
    import models  # noqa: F401
    db.create_all()
    
    # Create default admin user if no users exist
    from models import User
    if User.query.count() == 0:
        admin_user = User(
            username='admin',
            email='admin@gstbilling.com',
            first_name='System',
            last_name='Administrator',
            role='admin',
            is_active=True
        )
        admin_user.set_password('admin123')  # Default password
        db.session.add(admin_user)
        db.session.commit()
        logging.info("Default admin user created: username='admin', password='admin123'")

# Import routes
import routes  # noqa: F401
import field_routes  # noqa: F401

# Initialize default fields
from field_utils import initialize_default_fields
with app.app_context():
    initialize_default_fields()
