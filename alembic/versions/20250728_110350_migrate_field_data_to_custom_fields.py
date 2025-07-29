"""Migrate field data to custom_fields

Revision ID: b74f1da53ff2
Revises: b9386c636d88
Create Date: 2025-07-28 11:03:50.652319

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import JSON

# revision identifiers, used by Alembic.
revision = 'b74f1da53ff2'
down_revision = 'b9386c636d88'
branch_labels = None
depends_on = None

# Models for the migration
Base = declarative_base()

class FieldDefinition(Base):
    __tablename__ = 'field_definition'
    id = sa.Column(sa.Integer, primary_key=True)
    entity_type = sa.Column(sa.String(50), nullable=False)
    field_name = sa.Column(sa.String(50), nullable=False)
    field_type = sa.Column(sa.String(20), nullable=False)
    options = sa.Column(sa.Text)

class FieldData(Base):
    __tablename__ = 'field_data'
    id = sa.Column(sa.Integer, primary_key=True)
    field_definition_id = sa.Column(sa.Integer, sa.ForeignKey('field_definition.id'), nullable=False)
    entity_id = sa.Column(sa.Integer, nullable=False)
    value_text = sa.Column(sa.Text)
    value_number = sa.Column(sa.Numeric(15, 5))
    value_date = sa.Column(sa.DateTime)
    value_boolean = sa.Column(sa.Boolean)

def get_value(field_data, field_type):
    """Get the field value based on field type"""
    if field_type == 'text' or field_type == 'select':
        return field_data.value_text
    elif field_type == 'number':
        return float(field_data.value_number) if field_data.value_number is not None else None
    elif field_type == 'date':
        return field_data.value_date.isoformat() if field_data.value_date is not None else None
    elif field_type == 'boolean':
        return field_data.value_boolean
    return None

def upgrade() -> None:
    # Create a connection and bind a session
    connection = op.get_bind()
    Session = sessionmaker(bind=connection)
    session = Session()
    
    try:
        # Get all field definitions
        field_defs = session.query(FieldDefinition).all()
        
        # Group field definitions by entity type
        field_defs_by_type = {}
        for field_def in field_defs:
            if field_def.entity_type not in field_defs_by_type:
                field_defs_by_type[field_def.entity_type] = []
            field_defs_by_type[field_def.entity_type].append(field_def)
        
        # Process each entity type
        for entity_type, field_defs in field_defs_by_type.items():
            # Get table name based on entity type
            table_name = entity_type
            if entity_type == 'product':
                table_name = 'product'
            elif entity_type == 'customer':
                table_name = 'customer'
            elif entity_type == 'company':
                table_name = 'company_config'
            elif entity_type == 'user':
                table_name = 'users'
            elif entity_type == 'bill':
                table_name = 'bill'
            elif entity_type == 'bill_item':
                table_name = 'bill_item'
            elif entity_type == 'category':
                table_name = 'category'
            
            # Create a field ID to name map
            field_name_map = {fd.id: fd.field_name for fd in field_defs}
            field_type_map = {fd.id: fd.field_type for fd in field_defs}
            
            # Get all entity IDs for this type
            entity_ids_query = text(f"SELECT id FROM {table_name}")
            entity_ids = [row[0] for row in connection.execute(entity_ids_query)]
            
            # For each entity, collect field data and update custom_fields
            for entity_id in entity_ids:
                # Get all field data for this entity
                field_data_items = session.query(FieldData).filter(
                    FieldData.field_definition_id.in_(field_name_map.keys()),
                    FieldData.entity_id == entity_id
                ).all()
                
                # Skip if no field data
                if not field_data_items:
                    continue
                
                # Build the custom_fields JSON
                custom_fields = {}
                for fd in field_data_items:
                    field_name = field_name_map.get(fd.field_definition_id)
                    field_type = field_type_map.get(fd.field_definition_id)
                    if field_name:
                        custom_fields[field_name] = get_value(fd, field_type)
                
                # Skip if no custom fields to update
                if not custom_fields:
                    continue
                
                # Update the entity's custom_fields column
                update_query = text(
                    f"UPDATE {table_name} SET custom_fields = :custom_fields WHERE id = :id"
                )
                connection.execute(update_query, {
                    'custom_fields': json.dumps(custom_fields), 
                    'id': entity_id
                })
        
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def downgrade() -> None:
    # We don't need to undo the data migration since the FieldData table still exists
    pass
