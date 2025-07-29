"""
Schema Validation Script

This script checks for any discrepancies between the SQLAlchemy models
and the actual database schema, helping to identify potential issues
before they cause runtime errors.
"""

from app import app, db
from sqlalchemy import inspect
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_table_exists(table_name):
    """Check if a table exists in the database"""
    inspector = inspect(db.engine)
    return table_name in inspector.get_table_names()

def check_column_exists(table_name, column_name):
    """Check if a column exists in a table"""
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def validate_model(model):
    """Validate a model against the database schema"""
    table_name = model.__tablename__
    if not check_table_exists(table_name):
        logger.error(f"Table '{table_name}' does not exist in the database")
        return False
    
    inspector = inspect(db.engine)
    db_columns = {col['name'] for col in inspector.get_columns(table_name)}
    model_columns = {col.name for col in model.__table__.columns}
    
    # Find columns in model but not in database
    missing_columns = model_columns - db_columns
    if missing_columns:
        logger.error(f"Table '{table_name}' is missing columns: {missing_columns}")
        
    # Find columns in database but not in model
    extra_columns = db_columns - model_columns
    if extra_columns:
        logger.warning(f"Table '{table_name}' has extra columns not in model: {extra_columns}")
    
    return not missing_columns

def validate_all_models():
    """Validate all models against the database schema"""
    from models import User, Company, Customer, Product, Bill, BillItem, BillSequence, Category
    
    models = [
        User, 
        Company, 
        Customer, 
        Product, 
        Bill, 
        BillItem, 
        BillSequence, 
        Category
    ]
    
    all_valid = True
    for model in models:
        logger.info(f"Validating model: {model.__name__}")
        if not validate_model(model):
            all_valid = False
    
    return all_valid

if __name__ == "__main__":
    with app.app_context():
        logger.info("Starting schema validation...")
        if validate_all_models():
            logger.info("All models validated successfully!")
        else:
            logger.warning("Schema validation found issues. See above for details.")
