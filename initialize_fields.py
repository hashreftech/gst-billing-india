from app import app
from models import FieldDefinition
from extensions import db
from sqlalchemy.exc import SQLAlchemyError

def initialize_product_fields():
    """Initialize and enable default product fields"""
    try:
        with app.app_context():
            # Define default product fields
            product_fields = [
                {
                    "field_name": "serial_number",
                    "display_name": "Serial Number",
                    "field_type": "text",
                    "field_order": 1,
                    "enabled": True,
                    "help_text": "Product serial number or SKU"
                },
                {
                    "field_name": "width",
                    "display_name": "Width (cm)",
                    "field_type": "number",
                    "field_order": 2,
                    "enabled": True,
                    "help_text": "Product width in centimeters"
                },
                {
                    "field_name": "length",
                    "display_name": "Length (cm)",
                    "field_type": "number",
                    "field_order": 3,
                    "enabled": True,
                    "help_text": "Product length in centimeters"
                },
                {
                    "field_name": "height",
                    "display_name": "Height (cm)",
                    "field_type": "number",
                    "field_order": 4,
                    "enabled": True,
                    "help_text": "Product height in centimeters"
                },
                {
                    "field_name": "weight",
                    "display_name": "Weight (kg)",
                    "field_type": "number",
                    "field_order": 5,
                    "enabled": True,
                    "help_text": "Product weight in kilograms"
                },
                {
                    "field_name": "color",
                    "display_name": "Color",
                    "field_type": "text",
                    "field_order": 6,
                    "enabled": True,
                    "help_text": "Product color"
                },
                {
                    "field_name": "material",
                    "display_name": "Material",
                    "field_type": "text",
                    "field_order": 7,
                    "enabled": True,
                    "help_text": "Product material"
                }
            ]

            # Process each field
            for field_data in product_fields:
                # Check if field exists
                field = FieldDefinition.query.filter_by(
                    entity_type='product',
                    field_name=field_data["field_name"]
                ).first()

                # Create or update the field
                if not field:
                    field = FieldDefinition(
                        entity_type='product',
                        field_name=field_data["field_name"],
                        display_name=field_data["display_name"],
                        field_type=field_data["field_type"],
                        field_order=field_data["field_order"],
                        enabled=field_data["enabled"],
                        help_text=field_data["help_text"]
                    )
                    db.session.add(field)
                else:
                    # Update existing field
                    field.display_name = field_data["display_name"]
                    field.field_type = field_data["field_type"]
                    field.field_order = field_data["field_order"]
                    field.enabled = field_data["enabled"]
                    field.help_text = field_data["help_text"]

            # Commit all changes
            db.session.commit()
            print("Successfully initialized product fields!")
            return True

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Database error initializing product fields: {str(e)}")
        return False
    except Exception as e:
        db.session.rollback()
        print(f"Error initializing product fields: {str(e)}")
        return False

if __name__ == "__main__":
    initialize_product_fields()
