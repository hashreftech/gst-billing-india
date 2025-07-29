"""
Product utility functions to manage product field settings.

This module contains functions to work with the dynamic product fields
that can be enabled or disabled from settings.
"""

from app import db
from models import ProductFieldSettings

def get_enabled_product_fields():
    """
    Returns a list of enabled product fields from the database.
    
    Returns:
        list: A list of ProductFieldSettings objects for enabled fields.
    """
    try:
        return ProductFieldSettings.query.filter_by(is_enabled=True).order_by(ProductFieldSettings.field_order).all()
    except Exception as e:
        print(f"Error getting enabled product fields: {str(e)}")
        return []

def get_product_field_by_name(field_name):
    """
    Get a product field setting by its field name.
    
    Args:
        field_name (str): The name of the field to retrieve.
        
    Returns:
        ProductFieldSettings: The field setting object or None if not found.
    """
    try:
        return ProductFieldSettings.query.filter_by(field_name=field_name).first()
    except Exception as e:
        print(f"Error getting product field {field_name}: {str(e)}")
        return None

def update_product_field_status(field_name, is_enabled):
    """
    Update the enabled status of a product field.
    
    Args:
        field_name (str): The name of the field to update.
        is_enabled (bool): Whether the field should be enabled.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        field = ProductFieldSettings.query.filter_by(field_name=field_name).first()
        if field:
            field.is_enabled = is_enabled
            db.session.commit()
            return True
        return False
    except Exception as e:
        db.session.rollback()
        print(f"Error updating product field {field_name}: {str(e)}")
        return False

def initialize_product_fields():
    """
    Initialize default product fields if they don't exist.
    This should be called during application startup.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Define default fields
        default_fields = [
            {"field_name": "serial_number", "display_name": "Serial Number", "field_type": "text", "field_order": 1},
            {"field_name": "width", "display_name": "Width", "field_type": "number", "field_order": 2},
            {"field_name": "length", "display_name": "Length", "field_type": "number", "field_order": 3},
            {"field_name": "height", "display_name": "Height", "field_type": "number", "field_order": 4},
            {"field_name": "weight", "display_name": "Weight", "field_type": "number", "field_order": 5}
        ]
        
        # Check and create fields if they don't exist
        for field_data in default_fields:
            field = ProductFieldSettings.query.filter_by(field_name=field_data["field_name"]).first()
            if not field:
                field = ProductFieldSettings(
                    field_name=field_data["field_name"],
                    display_name=field_data["display_name"],
                    field_type=field_data["field_type"],
                    field_order=field_data["field_order"],
                    is_enabled=False
                )
                db.session.add(field)
        
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error initializing product fields: {str(e)}")
        return False
