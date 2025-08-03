from extensions import db
from datetime import datetime
from sqlalchemy import Text, JSON
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json

class Anonymous(AnonymousUserMixin):
    def is_admin(self):
        return False
    
    def is_manager(self):
        return False
        
    def has_role(self, role):
        return False

    def get_full_name(self):
        return "Guest"

    def get_custom_field_value(self, field_name):
        return None

class User(UserMixin, db.Model):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    role = db.Column(db.String(20), nullable=False, default='user')  # admin, manager, user
    is_active = db.Column(db.Boolean, default=True)
    custom_fields = db.Column(JSON, default=dict)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        if not password or not self.password_hash:  # Handle empty password or empty hash
            return False
        try:
            return check_password_hash(self.password_hash, password)
        except ValueError:  # Handle invalid hash format
            return False
    
    def has_role(self, role):
        """Check if user has specific role"""
        return self.role == role
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'
    
    def is_manager(self):
        """Check if user is manager or admin"""
        return self.role in ['admin', 'manager']
    
    def get_full_name(self):
        """Get user's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def get_custom_field_value(self, field_name):
        """Get a custom field value"""
        from field_utils import get_entity_field_value
        return get_entity_field_value('user', self.id, field_name)
    
    def set_custom_field_value(self, field_name, value):
        """Set a custom field value"""
        from field_utils import set_entity_field_value
        return set_entity_field_value('user', self.id, field_name, value)
    
    def get_all_custom_field_values(self):
        """Get all custom field values for this user"""
        from field_utils import get_all_entity_field_values
        return get_all_entity_field_values('user', self.id)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Company(db.Model):
    __tablename__ = 'company_config'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(Text, nullable=False)
    gst_number = db.Column(db.String(15), nullable=False)
    tan_number = db.Column(db.String(10))
    logo_path = db.Column(db.String(255))
    state_code = db.Column(db.String(2), nullable=False)
    custom_fields = db.Column(JSON, default=dict)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_custom_field_value(self, field_name):
        """Get a custom field value"""
        from field_utils import get_entity_field_value
        return get_entity_field_value('company', self.id, field_name)
    
    def set_custom_field_value(self, field_name, value):
        """Set a custom field value"""
        from field_utils import set_entity_field_value
        return set_entity_field_value('company', self.id, field_name, value)
    
    def get_all_custom_field_values(self):
        """Get all custom field values for this company"""
        from field_utils import get_all_entity_field_values
        return get_all_entity_field_values('company', self.id)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(15))
    address = db.Column(Text)
    gst_number = db.Column(db.String(15))
    state_code = db.Column(db.String(2))
    is_guest = db.Column(db.Boolean, default=False)
    custom_fields = db.Column(JSON, default=dict)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with bills
    bills = db.relationship('Bill', backref='customer', lazy=True)
    
    def get_custom_field_value(self, field_name):
        """Get a custom field value"""
        from field_utils import get_entity_field_value
        return get_entity_field_value('customer', self.id, field_name)
    
    def set_custom_field_value(self, field_name, value):
        """Set a custom field value"""
        from field_utils import set_entity_field_value
        return set_entity_field_value('customer', self.id, field_name, value)
    
    def get_all_custom_field_values(self):
        """Get all custom field values for this customer"""
        from field_utils import get_all_entity_field_values
        return get_all_entity_field_values('customer', self.id)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    hsn_code = db.Column(db.String(10), nullable=False)
    gst_rate = db.Column(db.Numeric(5, 2), nullable=False, default=18.0)  # Total GST rate (for backward compatibility)
    cgst_rate = db.Column(db.Numeric(5, 2), nullable=False, default=9.0)  # CGST component
    sgst_rate = db.Column(db.Numeric(5, 2), nullable=False, default=9.0)  # SGST component
    unit = db.Column(db.String(20), default='Nos')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    custom_fields = db.Column(JSON, default=dict)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with category
    category = db.relationship('Category', backref='products')
    
    def get_custom_field_value(self, field_name):
        """Get a custom field value"""
        from field_utils import get_entity_field_value
        return get_entity_field_value('product', self.id, field_name)
    
    def set_custom_field_value(self, field_name, value):
        """Set a custom field value"""
        from field_utils import set_entity_field_value
        return set_entity_field_value('product', self.id, field_name, value)
    
    def get_all_custom_field_values(self):
        """Get all custom field values for this product"""
        from field_utils import get_all_entity_field_values
        return get_all_entity_field_values('product', self.id)

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    bill_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.Date)
    subtotal = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    discount_type = db.Column(db.String(10), default='none')  # 'none', 'percentage', 'amount'
    discount_value = db.Column(db.Numeric(12, 2), default=0)
    discount_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    gst_amount = db.Column(db.Numeric(12, 2), nullable=True)  # Legacy column
    cgst_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    sgst_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    igst_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    final_amount = db.Column(db.Numeric(12, 2), nullable=True)  # Legacy column
    total_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    created_by = db.Column(db.Integer, nullable=True)  # Legacy column
    notes = db.Column(Text)
    status = db.Column(db.String(20), default='Draft')  # Draft, Sent, Paid, Cancelled
    custom_fields = db.Column(JSON, default=dict)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with bill items
    items = db.relationship('BillItem', backref='bill', lazy=True, cascade='all, delete-orphan')
    
    def get_custom_field_value(self, field_name):
        """Get a custom field value"""
        from field_utils import get_entity_field_value
        return get_entity_field_value('bill', self.id, field_name)
    
    def set_custom_field_value(self, field_name, value):
        """Set a custom field value"""
        from field_utils import set_entity_field_value
        return set_entity_field_value('bill', self.id, field_name, value)
    
    def get_all_custom_field_values(self):
        """Get all custom field values for this bill"""
        from field_utils import get_all_entity_field_values
        return get_all_entity_field_values('bill', self.id)

class BillItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bill_id = db.Column(db.Integer, db.ForeignKey('bill.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product_name = db.Column(db.String(200), nullable=False)
    description = db.Column(Text)
    hsn_code = db.Column(db.String(10), nullable=False)
    quantity = db.Column(db.Numeric(10, 3), nullable=False, default=1)
    unit = db.Column(db.String(20), default='Nos')
    unit_price = db.Column(db.Numeric(10, 2), nullable=True)  # Legacy column
    rate = db.Column(db.Numeric(10, 2), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    discount_percent = db.Column(db.Numeric(5, 2), nullable=True)  # Legacy column
    discount_amount = db.Column(db.Numeric(12, 2), nullable=True)  # Legacy column
    taxable_amount = db.Column(db.Numeric(12, 2), nullable=True)  # Legacy column
    gst_rate = db.Column(db.Numeric(5, 2), nullable=False)
    cgst_rate = db.Column(db.Numeric(5, 2), nullable=False, default=0)  # CGST rate component
    sgst_rate = db.Column(db.Numeric(5, 2), nullable=False, default=0)  # SGST rate component
    gst_amount = db.Column(db.Numeric(12, 2), nullable=True)  # Legacy column
    cgst_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    sgst_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    igst_amount = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    total_amount = db.Column(db.Numeric(12, 2), nullable=True)  # Legacy column
    custom_fields = db.Column(JSON, default=dict)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)  # Legacy column
    updated_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)  # Legacy column
    
    # Relationship with product
    product = db.relationship('Product', backref='bill_items')
    
    def get_custom_field_value(self, field_name):
        """Get a custom field value"""
        from field_utils import get_entity_field_value
        return get_entity_field_value('bill_item', self.id, field_name)
    
    def set_custom_field_value(self, field_name, value):
        """Set a custom field value"""
        from field_utils import set_entity_field_value
        return set_entity_field_value('bill_item', self.id, field_name, value)
    
    def get_all_custom_field_values(self):
        """Get all custom field values for this bill item"""
        from field_utils import get_all_entity_field_values
        return get_all_entity_field_values('bill_item', self.id)

class BillSequence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    sequence_number = db.Column(db.Integer, nullable=False, default=0)
    
    __table_args__ = (db.UniqueConstraint('year', name='unique_year_sequence'),)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    custom_fields = db.Column(JSON, default=dict)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_custom_field_value(self, field_name):
        """Get a custom field value"""
        from field_utils import get_entity_field_value
        return get_entity_field_value('category', self.id, field_name)
    
    def set_custom_field_value(self, field_name, value):
        """Set a custom field value"""
        from field_utils import set_entity_field_value
        return set_entity_field_value('category', self.id, field_name, value)
    
    def get_all_custom_field_values(self):
        """Get all custom field values for this category"""
        from field_utils import get_all_entity_field_values
        return get_all_entity_field_values('category', self.id)

# Dynamic field system models
class FieldDefinition(db.Model):
    __tablename__ = 'field_definition'
    id = db.Column(db.Integer, primary_key=True)
    entity_type = db.Column(db.String(50), nullable=False)  # 'product', 'customer', etc.
    field_name = db.Column(db.String(50), nullable=False)
    display_name = db.Column(db.String(100), nullable=False)
    field_type = db.Column(db.String(20), nullable=False)  # 'text', 'number', 'date', 'boolean', 'select'
    required = db.Column(db.Boolean, default=False)
    searchable = db.Column(db.Boolean, default=False)
    enabled = db.Column(db.Boolean, default=True)
    field_order = db.Column(db.Integer, default=0)
    options = db.Column(Text)  # JSON string for select options
    default_value = db.Column(Text)
    validation_regex = db.Column(Text)
    help_text = db.Column(Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Ensure field_name is unique per entity_type
    __table_args__ = (db.UniqueConstraint('entity_type', 'field_name', name='uix_field_entity_name'),)
    
    # Relationship with field data
    field_data = db.relationship('FieldData', backref='field_definition', lazy=True, cascade='all, delete-orphan')
    
    @staticmethod
    def get_fields_for_entity(entity_type, enabled_only=True):
        """Get all fields for a specific entity type"""
        query = FieldDefinition.query.filter_by(entity_type=entity_type)
        if enabled_only:
            query = query.filter_by(enabled=True)
        return query.order_by(FieldDefinition.field_order).all()

class FieldData(db.Model):
    __tablename__ = 'field_data'
    id = db.Column(db.Integer, primary_key=True)
    field_definition_id = db.Column(db.Integer, db.ForeignKey('field_definition.id'), nullable=False)
    entity_id = db.Column(db.Integer, nullable=False)  # ID of the product, customer, etc.
    value_text = db.Column(Text)
    value_number = db.Column(db.Numeric(15, 5))
    value_date = db.Column(db.DateTime)
    value_boolean = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Ensure there's only one value per field per entity
    __table_args__ = (db.UniqueConstraint('field_definition_id', 'entity_id', name='uix_field_entity'),)
    
    def get_value(self):
        """Get the value in the appropriate type based on the field type"""
        field_type = self.field_definition.field_type
        
        if field_type == 'text' or field_type == 'select':
            return self.value_text
        elif field_type == 'number':
            return self.value_number
        elif field_type == 'date':
            return self.value_date
        elif field_type == 'boolean':
            return self.value_boolean
        return None
    
    def set_value(self, value):
        """Set the value in the appropriate column based on the field type"""
        field_type = self.field_definition.field_type
        
        if field_type == 'text' or field_type == 'select':
            self.value_text = value
        elif field_type == 'number':
            self.value_number = value
        elif field_type == 'date':
            self.value_date = value
        elif field_type == 'boolean':
            self.value_boolean = value

class FieldDefinitionHistory(db.Model):
    __tablename__ = 'field_definition_history'
    id = db.Column(db.Integer, primary_key=True)
    field_definition_id = db.Column(db.Integer, db.ForeignKey('field_definition.id'), nullable=False)
    change_type = db.Column(db.String(20), nullable=False)  # 'create', 'update', 'delete'
    changed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    old_values = db.Column(JSON)
    new_values = db.Column(JSON)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with field definition
    field_definition = db.relationship('FieldDefinition')
    # Relationship with user
    user = db.relationship('User')
