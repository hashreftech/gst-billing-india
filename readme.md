# Indian GST Billing Software 🇮🇳

A simple, efficient, and compliant GST billing solution designed specifically for Indian businesses.

## Overview 📋

This billing software is tailored for Indian businesses, offering a straightforward way to manage products, generate GST-compliant invoices, and maintain proper business records. Built with small to medium businesses in mind, it provides all essential features while remaining easy to use.

## Key Features ⭐

- **GST-Compliant Billing**
  - Automatic GST calculations (CGST/SGST/IGST)
  - Support for all GST rates (0%, 5%, 12%, 18%, 28%)
  - HSN code management
  - State-wise GST handling

- **Product Management**
  - Easy product catalog management
  - Custom fields for product details
  - Category organization
  - Stock management
  - Bulk import/export

- **Customer Management**
  - Customer database with GST details
  - State code management
  - Custom fields for customer information
  - Customer history tracking

- **Business Tools**
  - Professional invoice generation
  - Business reports and analytics
  - GST return preparation aids
  - Daily/monthly/yearly sales reports

## Perfect For 👥

- Small retail shops
- Trading businesses
- Service providers
- Manufacturing units
- Wholesale businesses
- Any GST-registered business

## Business Benefits 💰

- **Compliance**: Stay compliant with GST regulations
- **Efficiency**: Save time with automated calculations
- **Organization**: Keep all business records organized
- **Professionalism**: Generate professional invoices
- **Insights**: Get valuable business insights through reports
- **Cost-Effective**: Free, open-source solution

## System Requirements

### 1. Install Python 3.11+
```bash
# Check if Python is installed
python3 --version

# If not installed, install via Homebrew
brew install python3
```

### 2. Install PostgreSQL
```bash
# Install PostgreSQL via Homebrew
brew install postgresql

# Start PostgreSQL service
brew services start postgresql

# Create a database
createdb gst_billing_db

# Create a user (optional)
psql gst_billing_db
CREATE USER gst_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE gst_billing_db TO gst_user;
\q
```

## Project Setup

### 1. Download/Clone the Project
Place all the project files in a directory, for example: `/Users/yourusername/gst-billing/`

### 2. Setup Options

#### Option A: Automated Setup (Recommended)

We've provided a setup script that automates most of the installation process:

```bash
# Make the script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

The script will:
1. Check for Python and PostgreSQL
2. Create a virtual environment
3. Install dependencies
4. Set up a sample `.env` file
5. Create the database (optional)
6. Run migrations (optional)
7. Create required directories

#### Option B: Manual Setup

##### Create Virtual Environment
```bash
cd /path/to/your/gst-billing/
python3 -m venv venv
source venv/bin/activate
```

##### Install Dependencies

#### Option A: Using pip with pyproject.toml (Recommended)
```bash
pip install -e .
```

#### Option B: Create requirements.txt and install manually
Create a `requirements.txt` file with these contents:
```
bcrypt==4.3.0
blinker==1.9.0
charset-normalizer==3.4.2
click==8.2.1
dnspython==2.7.0
email_validator==2.2.0
Flask==3.1.1
Flask-Login==0.6.3
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.2.2
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.2
pillow==11.3.0
psycopg2==2.9.10
python-dotenv==1.1.1
reportlab==4.4.3
SQLAlchemy==2.0.41
typing_extensions==4.14.1
Werkzeug==3.1.3
WTForms==3.2.1
alembic==1.13.1
openpyxl==3.1.2
gunicorn==23.0.0
```

Then install:
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in your project root:
```bash
# Database Configuration
DATABASE_URL=postgresql://pguser:pgpassword@localhost:5432/gst_billing_db

# Session Secret (generate a random string - required for authentication)
SESSION_SECRET=your-super-secret-key-here-change-this-in-production

# Flask Environment
FLASK_ENV=development
FLASK_DEBUG=True

### 5. Load Environment Variables
Install python-dotenv and modify your app:
```bash
pip install python-dotenv
```

Add to the top of `app.py`:
```python
from dotenv import load_dotenv
load_dotenv()  # Add this line at the top
```

## Database Management

The application uses Alembic for database migrations. This allows for:
- Tracking database schema changes in version control
- Upgrading or downgrading the database schema to specific versions
- Resetting the database to a clean state without losing schema information

For detailed information on managing the database, see [Database Migrations Documentation](docs/database_migrations.md).

## Running the Application

### Option 1: Development Server
```bash
source venv/bin/activate
python main.py
```

### Option 2: Production-like with Gunicorn
```bash
source venv/bin/activate
gunicorn --bind 127.0.0.1:5000 --reload main:app
```

The application will be available at: `http://localhost:5000`

## Default Login
- **Username:** admin
- **Password:** admin123

## Troubleshooting

### Database Connection Issues
1. Ensure PostgreSQL is running: `brew services start postgresql`
2. Check database exists: `psql -l | grep gst_billing`
3. Test connection: `psql gst_billing_db`

### Permission Issues
1. Check file permissions: `chmod +x main.py`
2. Ensure uploads directory exists: `mkdir uploads`

### PDF Generation Issues
If you see black boxes instead of rupee symbols (₹) in PDF invoices:

1. The application has been updated to use DejaVu fonts, which properly support the rupee symbol
2. Make sure all DejaVu font files are installed in the `static/fonts/` directory
3. If you still see issues:
   - Open `pdf_generator.py` and set `USE_FALLBACK_CURRENCY = True` near the top of the file
   - This will use "Rs." notation instead of the rupee symbol
4. You can download DejaVu fonts from their official GitHub repository if needed:
   - https://github.com/dejavu-fonts/dejavu-fonts/releases

### Port Already in Use
If port 5000 is busy, change it in main.py or use:
```bash
gunicorn --bind 127.0.0.1:8000 --reload main:app
```

## Security Notes
- Change the default admin password immediately after first login
- Use a strong SESSION_SECRET in production
- Consider using environment-specific configuration files
- Enable firewall rules for production deployment

## Database Migrations

This project uses a custom migration system to manage database schema changes.

### Complete Initial Database Setup

For a fresh installation, you can use our comprehensive migration script that sets up the entire database structure:

```bash
# Create the database if it doesn't exist
createdb gst_billing_db

# Apply the initial database schema
python migrations/20250728120000_initial_schema_setup.py
```
## Database Management

This application uses Alembic for database migrations, wrapped in a custom `db_manage.py` script for ease of use.

### Available Commands

```bash
# Initialize a fresh database with all tables
python db_manage.py init

# Reset the database (drops all tables and recreates them)
python db_manage.py reset

# Apply all unapplied migrations
python db_manage.py upgrade

# Downgrade to a specific revision
python db_manage.py downgrade revision_id

# Create a new migration
python db_manage.py revision "Description of changes"
```

### Dynamic Custom Fields System

This project implements a flexible, Drupal-like system for adding custom fields to entities:

1. **Custom Field Types**: The application supports various field types:
   - Text fields
   - Number fields
   - Date fields
   - Boolean fields
   - Select fields with options

2. **Field Management**: Administrators can:
   - Create new custom fields for products, customers, etc.
   - Configure field properties (required, validation, help text)
   - Enable/disable fields
   - Set field order in forms

3. **Using Custom Fields**: Access custom field values in code:
   ```python
   # Get a custom field value
   product.get_custom_field_value('color')
   
   # Set a custom field value
   product.set_custom_field_value('width', 10.5)
   
   # Get all custom fields for a product
   all_fields = product.get_all_custom_field_values()
   ```

4. **Database Structure**: Custom fields use a flexible JSON-based structure:
   - `field_definition`: Stores metadata about fields
   - Entity tables have a `custom_fields` JSON column for efficient storage
   - `field_definition_history`: Tracks changes to field definitions

5. **Implementing Custom Fields for New Entities**:
   To add custom fields support to a new entity:
   
   ```python
   class YourEntity(db.Model):
       # Regular fields
       id = db.Column(db.Integer, primary_key=True)
       name = db.Column(db.String(100))
       
       # Add custom_fields JSON column
       custom_fields = db.Column(JSON, default=dict)
       
       # Add helper methods
       def get_custom_field_value(self, field_name):
           from field_utils import get_entity_field_value
           return get_entity_field_value('your_entity_type', self.id, field_name)
       
       def set_custom_field_value(self, field_name, value):
           from field_utils import set_entity_field_value
           return set_entity_field_value('your_entity_type', self.id, field_name, value)
       
       def get_all_custom_field_values(self):
           from field_utils import get_all_entity_field_values
           return get_all_entity_field_values('your_entity_type', self.id)
   ```

## Features Available

### Web Application Features
- ✅ User Authentication & Role Management (Admin, Manager, User)
- ✅ Company Configuration with GST Details
- ✅ Customer Management with GST Number Validation
- ✅ Product Catalog with HSN Codes and GST Rates
- ✅ Dynamic Custom Fields for Products, Customers, Bills, etc.
- ✅ Invoice Creation with Automatic GST Calculations
- ✅ Discount System (Percentage and Fixed Amount)
- ✅ Bill Status Management (Draft, Sent, Paid, Cancelled)
- ✅ PDF Invoice Generation
- ✅ Excel Export Functionality
- ✅ Advanced Search and Filtering
- ✅ Dashboard with Business Analytics
