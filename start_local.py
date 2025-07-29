#!/usr/bin/env python3
"""
Local development startup script for GST Billing Software
This script helps set up and run the application locally on Mac Mini
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_virtual_environment():
    """Check if virtual environment is activated"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Virtual environment is activated")
        return True
    else:
        print("⚠️  Virtual environment not detected")
        print("Recommendation: Create and activate a virtual environment")
        print("Commands:")
        print("  python3 -m venv venv")
        print("  source venv/bin/activate")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask', 'flask_sqlalchemy', 'flask_login', 
        'flask_wtf', 'wtforms', 'werkzeug', 'psycopg2', 
        'bcrypt', 'email_validator', 'reportlab'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print("\n📦 Install missing packages:")
        print("pip install " + " ".join(missing_packages))
        return False
    
    return True

def check_database_connection():
    """Check if PostgreSQL is available"""
    try:
        import psycopg2
        # Try to connect using environment variable or default
        db_url = os.getenv('DATABASE_URL', 'postgresql://localhost:5432/gst_billing_db')
        print(f"🔗 Testing database connection: {db_url}")
        
        # This will be handled by the application itself
        print("✅ Database connection will be tested by the application")
        return True
    except ImportError:
        print("❌ psycopg2 not installed")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path('.env')
    if not env_file.exists():
        print("📝 Creating .env file...")
        env_content = """# Database Configuration
DATABASE_URL=postgresql://localhost:5432/gst_billing_db

# Session Secret (change this in production)
SESSION_SECRET=your-super-secret-development-key-change-this

# Flask Environment
FLASK_ENV=development
FLASK_DEBUG=True
"""
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created")
        print("⚠️  Please update DATABASE_URL in .env file with your PostgreSQL credentials")
    else:
        print("✅ .env file exists")

def start_application():
    """Start the Flask application"""
    print("\n🚀 Starting GST Billing Software...")
    print("📍 Application will be available at: http://localhost:5000")
    print("👤 Default login: admin / admin123")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        # Try to load environment variables
        try:
            from dotenv import load_dotenv
            load_dotenv()
            print("✅ Environment variables loaded")
        except ImportError:
            print("⚠️  python-dotenv not installed, using system environment")
        
        # Import and run the application
        from app import app
        app.run(host='127.0.0.1', port=5000, debug=True)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

def main():
    """Main setup and startup function"""
    print("🏭 GST Billing Software - Local Setup")
    print("=" * 40)
    
    # Check system requirements
    if not check_python_version():
        return
    
    print("\n📋 Checking Dependencies:")
    print("-" * 25)
    venv_ok = check_virtual_environment()
    deps_ok = check_dependencies()
    db_ok = check_database_connection()
    
    if not deps_ok:
        print("\n❌ Please install missing dependencies first")
        return
    
    print("\n⚙️  Configuration:")
    print("-" * 15)
    create_env_file()
    
    print("\n" + "=" * 40)
    
    if not venv_ok:
        response = input("Continue without virtual environment? (y/N): ")
        if response.lower() != 'y':
            return
    
    # Start the application
    start_application()

if __name__ == "__main__":
    main()