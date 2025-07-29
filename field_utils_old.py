"""
Utility functions for working with dynamic custom fields using JSON columns.

This module provides helper functions to interact with the dynamic field system,
making it easier to get and set field values for different entity types.
This version uses the custom_fields JSON column in models for storage.
"""

from extensions import db
from models import FieldDefinition, User, Product, Customer, Company, Category, Bill, BillItem
from flask import current_app
import json
from sqlalchemy.exc import SQLAlchemyError

# Model mapping dictionary to get the correct model class for an entity type
MODEL_MAP = {
    'product': Product,
    'customer': Customer,
    'company': Company,
    'category': Category,
    'user': User,
    'bill': Bill,
    'bill_item': BillItem
}

def get_entity_field_value(entity_type, entity_id, field_name):
    """
    Get a field value for a specific entity using the custom_fields JSON column.
    
    Args:
        entity_type (str): The type of entity ('product', 'customer', etc.)
        entity_id (int): The ID of the entity
        field_name (str): The name of the field to get
        
    Returns:
        The field value in its appropriate type, or None if not found
    """
    try:
        # Get the model class for this entity type
        model_class = MODEL_MAP.get(entity_type)
        if not model_class:
            current_app.logger.error(f"Unknown entity type: {entity_type}")
            return None
        
        # Find the entity
        entity = model_class.query.get(entity_id)
        if not entity:
            current_app.logger.error(f"Entity not found: {entity_type} #{entity_id}")
            return None
        
        # Check if the entity has a custom_fields attribute
        if not hasattr(entity, 'custom_fields') or not entity.custom_fields:
            return None
        
        # Get the value from the custom_fields JSON
        return entity.custom_fields.get(field_name)
    
    except Exception as e:
        current_app.logger.error(f"Error getting field value: {str(e)}")
        return None

def set_entity_field_value(entity_type, entity_id, field_name, value):
    """
    Set a field value for a specific entity using the custom_fields JSON column.
    
    Args:
        entity_type (str): The type of entity ('product', 'customer', etc.)
        entity_id (int): The ID of the entity
        field_name (str): The name of the field to set
        value: The value to set
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Validate the field exists and is enabled
        field_def = FieldDefinition.query.filter_by(
            entity_type=entity_type, 
            field_name=field_name,
            enabled=True
        ).first()
        
        if not field_def:
            current_app.logger.error(f"Field definition not found or disabled: {entity_type}.{field_name}")
            return False
        
        # Get the model class for this entity type
        model_class = MODEL_MAP.get(entity_type)
        if not model_class:
            current_app.logger.error(f"Unknown entity type: {entity_type}")
            return False
        
        # Find the entity
        entity = model_class.query.get(entity_id)
        if not entity:
            current_app.logger.error(f"Entity not found: {entity_type} #{entity_id}")
            return False
        
        # Initialize custom_fields as an empty dict if it's None
        if entity.custom_fields is None:
            entity.custom_fields = {}
        
        # Update the custom_fields JSON with the new value
        custom_fields = dict(entity.custom_fields)  # Create a copy to avoid reference issues
        custom_fields[field_name] = value
        entity.custom_fields = custom_fields
        
        # Save changes
        db.session.commit()
        return True
    
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error setting field value: {str(e)}")
        return False
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error setting field value: {str(e)}")
        return False

def get_all_entity_field_values(entity_type, entity_id):
    """
    Get all field values for a specific entity using the custom_fields JSON column.
    
    Args:
        entity_type (str): The type of entity ('product', 'customer', etc.)
        entity_id (int): The ID of the entity
        
    Returns:
        dict: A dictionary of field names and their values
    """
    try:
        # Get the model class for this entity type
        model_class = MODEL_MAP.get(entity_type)
        if not model_class:
            current_app.logger.error(f"Unknown entity type: {entity_type}")
            return {}
        
        # Find the entity
        entity = model_class.query.get(entity_id)
        if not entity:
            current_app.logger.error(f"Entity not found: {entity_type} #{entity_id}")
            return {}
        
        # Return a copy of the custom_fields JSON or an empty dict if None
        return dict(entity.custom_fields or {})
    
    except Exception as e:
        current_app.logger.error(f"Error getting all field values: {str(e)}")
        return {}

def create_field_definition(entity_type, field_name, display_name, field_type, 
                           required=False, enabled=True, field_order=0,
                           options=None, default_value=None, validation_regex=None,
                           help_text=None, user_id=None):
    """
    Create a new field definition.
    
    Args:
        entity_type (str): The type of entity ('product', 'customer', etc.)
        field_name (str): The name of the field (for database use)
        display_name (str): The human-readable name of the field
        field_type (str): The type of field ('text', 'number', 'date', 'boolean', 'select')
        required (bool): Whether the field is required
        enabled (bool): Whether the field is enabled
        field_order (int): The order of the field in forms
        options (list): List of options for select fields
        default_value: The default value for the field
        validation_regex (str): A regex pattern for validation
        help_text (str): Help text for the field
        user_id (int): The ID of the user creating the field
        
    Returns:
        FieldDefinition: The created field definition, or None if failed
    """
    try:
        # Check if a field with this name already exists
        existing = FieldDefinition.query.filter_by(
            entity_type=entity_type,
            field_name=field_name
        ).first()
        
        if existing:
            current_app.logger.error(f"Field already exists: {entity_type}.{field_name}")
            return None
        
        # Convert options to JSON if provided
        options_json = json.dumps(options) if options else None
        
        # Create the field definition
        field_def = FieldDefinition(
            entity_type=entity_type,
            field_name=field_name,
            display_name=display_name,
            field_type=field_type,
            required=required,
            enabled=enabled,
            field_order=field_order,
            options=options_json,
            default_value=default_value,
            validation_regex=validation_regex,
            help_text=help_text
        )
        
        db.session.add(field_def)
        db.session.commit()
        
        # Create history record if user_id is provided
        if user_id:
            from models import FieldDefinitionHistory
            history = FieldDefinitionHistory(
                field_definition_id=field_def.id,
                change_type='create',
                changed_by=user_id,
                new_values={
                    'entity_type': entity_type,
                    'field_name': field_name,
                    'display_name': display_name,
                    'field_type': field_type,
                    'required': required,
                    'enabled': enabled,
                    'field_order': field_order,
                    'options': options,
                    'default_value': default_value,
                    'validation_regex': validation_regex,
                    'help_text': help_text
                }
            )
            db.session.add(history)
            db.session.commit()
        
        return field_def
    
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error creating field definition: {str(e)}")
        return None
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error creating field definition: {str(e)}")
        return None

def update_field_definition(field_id, display_name=None, field_type=None, 
                           required=None, enabled=None, field_order=None,
                           options=None, default_value=None, validation_regex=None,
                           help_text=None, user_id=None):
    """
    Update an existing field definition.
    
    Args:
        field_id (int): The ID of the field definition to update
        display_name (str): The human-readable name of the field
        field_type (str): The type of field ('text', 'number', 'date', 'boolean', 'select')
        required (bool): Whether the field is required
        enabled (bool): Whether the field is enabled
        field_order (int): The order of the field in forms
        options (list): List of options for select fields
        default_value: The default value for the field
        validation_regex (str): A regex pattern for validation
        help_text (str): Help text for the field
        user_id (int): The ID of the user updating the field
        
    Returns:
        FieldDefinition: The updated field definition, or None if failed
    """
    try:
        # Find the field definition
        field_def = FieldDefinition.query.get(field_id)
        if not field_def:
            current_app.logger.error(f"Field definition not found: {field_id}")
            return None
        
        # Store the old values for history
        old_values = {
            'display_name': field_def.display_name,
            'field_type': field_def.field_type,
            'required': field_def.required,
            'enabled': field_def.enabled,
            'field_order': field_def.field_order,
            'options': json.loads(field_def.options) if field_def.options else None,
            'default_value': field_def.default_value,
            'validation_regex': field_def.validation_regex,
            'help_text': field_def.help_text
        }
        
        # Update the field definition
        if display_name is not None:
            field_def.display_name = display_name
        if field_type is not None:
            field_def.field_type = field_type
        if required is not None:
            field_def.required = required
        if enabled is not None:
            field_def.enabled = enabled
        if field_order is not None:
            field_def.field_order = field_order
        if options is not None:
            field_def.options = json.dumps(options)
        if default_value is not None:
            field_def.default_value = default_value
        if validation_regex is not None:
            field_def.validation_regex = validation_regex
        if help_text is not None:
            field_def.help_text = help_text
        
        # Store the new values for history
        new_values = {
            'display_name': field_def.display_name,
            'field_type': field_def.field_type,
            'required': field_def.required,
            'enabled': field_def.enabled,
            'field_order': field_def.field_order,
            'options': json.loads(field_def.options) if field_def.options else None,
            'default_value': field_def.default_value,
            'validation_regex': field_def.validation_regex,
            'help_text': field_def.help_text
        }
        
        # Save changes
        db.session.commit()
        
        # Create history record if user_id is provided
        if user_id:
            from models import FieldDefinitionHistory
            history = FieldDefinitionHistory(
                field_definition_id=field_id,
                change_type='update',
                changed_by=user_id,
                old_values=old_values,
                new_values=new_values
            )
            db.session.add(history)
            db.session.commit()
        
        return field_def
    
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error updating field definition: {str(e)}")
        return None
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error updating field definition: {str(e)}")
        return None

def delete_field_definition(field_id, user_id=None):
    """
    Delete a field definition.
    
    Args:
        field_id (int): The ID of the field definition to delete
        user_id (int): The ID of the user deleting the field
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Find the field definition
        field_def = FieldDefinition.query.get(field_id)
        if not field_def:
            current_app.logger.error(f"Field definition not found: {field_id}")
            return False
        
        # Store the values for history
        old_values = {
            'entity_type': field_def.entity_type,
            'field_name': field_def.field_name,
            'display_name': field_def.display_name,
            'field_type': field_def.field_type,
            'required': field_def.required,
            'enabled': field_def.enabled,
            'field_order': field_def.field_order,
            'options': json.loads(field_def.options) if field_def.options else None,
            'default_value': field_def.default_value,
            'validation_regex': field_def.validation_regex,
            'help_text': field_def.help_text
        }
        
        # Create history record if user_id is provided
        if user_id:
            from models import FieldDefinitionHistory
            history = FieldDefinitionHistory(
                field_definition_id=field_id,
                change_type='delete',
                changed_by=user_id,
                old_values=old_values
            )
            db.session.add(history)
        
        # Delete the field definition
        db.session.delete(field_def)
        db.session.commit()
        
        return True
    
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error deleting field definition: {str(e)}")
        return False
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting field definition: {str(e)}")
        return False

def migrate_field_data_to_json():
    """
    Migrate existing field data from the FieldData table to custom_fields JSON columns.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from models import FieldData
        
        # Get all field definitions grouped by entity type
        field_defs_by_type = {}
        for field_def in FieldDefinition.query.all():
            if field_def.entity_type not in field_defs_by_type:
                field_defs_by_type[field_def.entity_type] = []
            field_defs_by_type[field_def.entity_type].append(field_def)
        
        # Process each entity type
        for entity_type, field_defs in field_defs_by_type.items():
            # Skip if the entity type is not in the MODEL_MAP
            if entity_type not in MODEL_MAP:
                current_app.logger.warning(f"Skipping unknown entity type: {entity_type}")
                continue
            
            # Get the model class for this entity type
            model_class = MODEL_MAP[entity_type]
            
            # Create a mapping of field_definition_id to field_name
            field_name_map = {fd.id: fd.field_name for fd in field_defs}
            
            # Get all entities of this type
            entities = model_class.query.all()
            
            # For each entity, get all its field data and update custom_fields
            for entity in entities:
                # Get all field data for this entity
                field_data_items = FieldData.query.filter(
                    FieldData.field_definition_id.in_(field_name_map.keys()),
                    FieldData.entity_id == entity.id
                ).all()
                
                # Skip if no field data
                if not field_data_items:
                    continue
                
                # Initialize custom_fields if None
                if entity.custom_fields is None:
                    entity.custom_fields = {}
                
                # Update custom_fields with field data values
                custom_fields = dict(entity.custom_fields)
                for fd in field_data_items:
                    field_name = field_name_map.get(fd.field_definition_id)
                    if field_name:
                        custom_fields[field_name] = fd.get_value()
                
                entity.custom_fields = custom_fields
            
            # Commit changes for this entity type
            db.session.commit()
        
        return True
    
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error migrating field data: {str(e)}")
        return False
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error migrating field data: {str(e)}")
        return False

def initialize_default_fields():
    """
    Initialize default fields for different entity types.
    This should be called during application startup.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Define default product fields
        product_fields = [
            {"field_name": "serial_number", "display_name": "Serial Number", "field_type": "text", "field_order": 1},
            {"field_name": "width", "display_name": "Width", "field_type": "number", "field_order": 2},
            {"field_name": "length", "display_name": "Length", "field_type": "number", "field_order": 3},
            {"field_name": "height", "display_name": "Height", "field_type": "number", "field_order": 4},
            {"field_name": "weight", "display_name": "Weight", "field_type": "number", "field_order": 5},
            {"field_name": "color", "display_name": "Color", "field_type": "text", "field_order": 6, "enabled": False},
            {"field_name": "material", "display_name": "Material", "field_type": "text", "field_order": 7, "enabled": False}
        ]
        
        # Initialize product fields
        for field_data in product_fields:
            # Check if field exists
            field = FieldDefinition.query.filter_by(
                entity_type='product',
                field_name=field_data["field_name"]
            ).first()
            
            # Create if it doesn't exist
            if not field:
                field = FieldDefinition(
                    entity_type='product',
                    field_name=field_data["field_name"],
                    display_name=field_data["display_name"],
                    field_type=field_data["field_type"],
                    field_order=field_data["field_order"],
                    enabled=field_data.get("enabled", True)
                )
                db.session.add(field)
        
        # Define default customer fields (can be expanded)
        customer_fields = [
            {"field_name": "website", "display_name": "Website", "field_type": "text", "field_order": 1, "enabled": False},
            {"field_name": "notes", "display_name": "Notes", "field_type": "text", "field_order": 2, "enabled": False}
        ]
        
        # Initialize customer fields
        for field_data in customer_fields:
            # Check if field exists
            field = FieldDefinition.query.filter_by(
                entity_type='customer',
                field_name=field_data["field_name"]
            ).first()
            
            # Create if it doesn't exist
            if not field:
                field = FieldDefinition(
                    entity_type='customer',
                    field_name=field_data["field_name"],
                    display_name=field_data["display_name"],
                    field_type=field_data["field_type"],
                    field_order=field_data["field_order"],
                    enabled=field_data.get("enabled", True)
                )
                db.session.add(field)
        
        db.session.commit()
        return True
    except SQLAlchemyError as e:
        db.session.rollback()
        current_app.logger.error(f"Database error initializing default fields: {str(e)}")
        return False
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error initializing default fields: {str(e)}")
        return False
