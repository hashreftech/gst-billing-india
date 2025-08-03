from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DecimalField, SelectField, BooleanField, DateField, HiddenField, FieldList, FormField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Length, Optional, NumberRange, Regexp, Email, EqualTo
from wtforms.widgets import TextArea
import re
import json
from models import Category

class CompanyConfigForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired(), Length(min=2, max=200)])
    address = TextAreaField('Address', validators=[DataRequired()], widget=TextArea())
    gst_number = StringField('GST Number', validators=[
        DataRequired(), 
        Length(min=15, max=15),
        Regexp(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}$', 
               message='Invalid GST number format')
    ])
    tan_number = StringField('TAN Number', validators=[
        Optional(),
        Length(min=10, max=10),
        Regexp(r'^[A-Z]{4}[0-9]{5}[A-Z]{1}$', message='Invalid TAN format')
    ])
    state_code = SelectField('State', validators=[DataRequired()], choices=[
        ('01', 'Jammu and Kashmir'), ('02', 'Himachal Pradesh'), ('03', 'Punjab'),
        ('04', 'Chandigarh'), ('05', 'Uttarakhand'), ('06', 'Haryana'),
        ('07', 'Delhi'), ('08', 'Rajasthan'), ('09', 'Uttar Pradesh'),
        ('10', 'Bihar'), ('11', 'Sikkim'), ('12', 'Arunachal Pradesh'),
        ('13', 'Nagaland'), ('14', 'Manipur'), ('15', 'Mizoram'),
        ('16', 'Tripura'), ('17', 'Meghalaya'), ('18', 'Assam'),
        ('19', 'West Bengal'), ('20', 'Jharkhand'), ('21', 'Odisha'),
        ('22', 'Chhattisgarh'), ('23', 'Madhya Pradesh'), ('24', 'Gujarat'),
        ('25', 'Daman and Diu'), ('26', 'Dadra and Nagar Haveli'),
        ('27', 'Maharashtra'), ('28', 'Andhra Pradesh'), ('29', 'Karnataka'),
        ('30', 'Goa'), ('31', 'Lakshadweep'), ('32', 'Kerala'),
        ('33', 'Tamil Nadu'), ('34', 'Puducherry'), ('35', 'Andaman and Nicobar Islands'),
        ('36', 'Telangana'), ('37', 'Andhra Pradesh (New)')
    ])
    logo = FileField('Company Logo', validators=[
        Optional(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])

class CustomerForm(FlaskForm):
    name = StringField('Customer Name', validators=[DataRequired(), Length(min=2, max=200)])
    email = StringField('Email', validators=[Optional()])
    phone = StringField('Phone', validators=[Optional(), Length(max=15)])
    address = TextAreaField('Address', validators=[Optional()], widget=TextArea())
    gst_number = StringField('GST Number', validators=[
        Optional(),
        Length(min=15, max=15),
        Regexp(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}[Z]{1}[0-9A-Z]{1}$', 
               message='Invalid GST number format')
    ])
    state_code = SelectField('State', validators=[Optional()], choices=[
        ('', 'Select State'),
        ('01', 'Jammu and Kashmir'), ('02', 'Himachal Pradesh'), ('03', 'Punjab'),
        ('04', 'Chandigarh'), ('05', 'Uttarakhand'), ('06', 'Haryana'),
        ('07', 'Delhi'), ('08', 'Rajasthan'), ('09', 'Uttar Pradesh'),
        ('10', 'Bihar'), ('11', 'Sikkim'), ('12', 'Arunachal Pradesh'),
        ('13', 'Nagaland'), ('14', 'Manipur'), ('15', 'Mizoram'),
        ('16', 'Tripura'), ('17', 'Meghalaya'), ('18', 'Assam'),
        ('19', 'West Bengal'), ('20', 'Jharkhand'), ('21', 'Odisha'),
        ('22', 'Chhattisgarh'), ('23', 'Madhya Pradesh'), ('24', 'Gujarat'),
        ('25', 'Daman and Diu'), ('26', 'Dadra and Nagar Haveli'),
        ('27', 'Maharashtra'), ('28', 'Andhra Pradesh'), ('29', 'Karnataka'),
        ('30', 'Goa'), ('31', 'Lakshadweep'), ('32', 'Kerala'),
        ('33', 'Tamil Nadu'), ('34', 'Puducherry'), ('35', 'Andaman and Nicobar Islands'),
        ('36', 'Telangana'), ('37', 'Andhra Pradesh (New)')
    ])
    is_guest = BooleanField('Guest Customer')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=200)])
    description = TextAreaField('Description', validators=[Optional()], widget=TextArea())
    price = DecimalField('Price', validators=[DataRequired()], places=2)
    hsn_code = StringField('HSN Code', validators=[DataRequired(), Length(min=4, max=10)])
    gst_rate = DecimalField('Total GST Rate (%)', validators=[DataRequired()], places=2, default=18.0)
    cgst_rate = DecimalField('CGST Rate (%)', validators=[DataRequired()], places=2, default=9.0)
    sgst_rate = DecimalField('SGST Rate (%)', validators=[DataRequired()], places=2, default=9.0)
    unit = StringField('Unit', validators=[DataRequired(), Length(max=20)], default='Nos')
    category = SelectField('Category', validators=[DataRequired()], coerce=str, choices=[])
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.custom_field_values = {}

    def set_category_choices(self):
        self.category.choices = [(c.id, c.category_name) for c in Category.query.all()]
        
    def add_custom_fields(self):
        """Add custom fields to the form based on enabled field definitions"""
        from models import FieldDefinition
        import json
        from flask import request
        
        # Get all enabled fields for products
        fields = FieldDefinition.query.filter_by(entity_type='product', enabled=True).order_by(FieldDefinition.field_order).all()
        
        # Debug prints
        print("Request form data:", request.form if request and request.form else "No form data")
        print("Current form data:", self.data)
        
        # Store original fields to preserve their order
        original_fields = list(self._fields.items())
        self._fields.clear()
        
        # First add back all the original fields
        for name, field in original_fields:
            self._fields[name] = field
            
        print("Custom field values before adding fields:", self.custom_field_values)  # Debug print
            
        # Add each custom field dynamically
        for field in fields:
            field_name = f"custom_{field.field_name}"
            validators = [Optional()]
            if field.required:
                validators = [DataRequired()]
            
            # Create the field class based on type
            field_class = None
            field_type = field.field_type.lower()
            field_kwargs = {
                'validators': validators,
                'label': field.display_name
            }
            
            if field_type == 'text':
                field_class = StringField
            elif field_type == 'textarea':
                field_class = TextAreaField
            elif field_type == 'number':
                field_class = DecimalField
                field_kwargs['places'] = 2
            elif field_type == 'boolean':
                field_class = BooleanField
            elif field_type == 'date':
                field_class = DateField
            elif field_type == 'select':
                field_class = SelectField
                choices = []
                if hasattr(field, 'options') and field.options:
                    try:
                        options = json.loads(field.options)
                    except json.JSONDecodeError:
                        options = field.options.strip().split('\n')
                    choices = [(opt.strip(), opt.strip()) for opt in options if opt.strip()]
                field_kwargs['choices'] = choices
            else:
                field_class = StringField
            
            if field_class:
                # Create an instance of the field and bind it to the form
                field_instance = field_class(**field_kwargs)
                field_instance = field_instance.bind(form=self, name=field_name)
                
                # Get the stored value for this field
                stored_value = self.custom_field_values.get(field.field_name)  # Use field.field_name instead of field_name
                print(f"Processing field {field_name} with stored value: {stored_value}, type: {type(stored_value)}")  # Debug print
                
                # Handle type conversion for stored values
                if stored_value is not None:
                    if field_type == 'number' and not isinstance(stored_value, (int, float, str)):
                        stored_value = str(stored_value)  # Convert to string for DecimalField
                    elif field_type == 'boolean' and isinstance(stored_value, str):
                        stored_value = stored_value.lower() in ('true', '1', 'yes', 'on')
                        
                print(f"After conversion - field {field_name}: value = {stored_value}, type = {type(stored_value)}")  # Debug print
                
                # Process the field with the stored value if available
                if stored_value is not None:
                    try:
                        field_instance.process(formdata=None, data=stored_value)
                    except Exception as e:
                        print(f"Error processing field {field_name}: {str(e)}")
                else:
                    field_instance.process(formdata=None)
                
                self._fields[field_name] = field_instance
                setattr(self, field_name, field_instance)
                print(f"Final field value for {field_name}: {field_instance.data}")  # Debug print
            
        return fields

class QuickAddProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=200)])
    price = DecimalField('Price', validators=[DataRequired()], places=2)
    hsn_code = StringField('HSN Code', validators=[DataRequired(), Length(min=4, max=10)])
    gst_rate = DecimalField('GST Rate (%)', validators=[DataRequired()], places=2, default=18.0)
    unit = StringField('Unit', validators=[DataRequired(), Length(max=20)], default='Nos')
    category = SelectField('Category', validators=[DataRequired()], coerce=int, choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category.choices = [(c.id, c.category_name) for c in Category.query.all()]

class BillItemForm(FlaskForm):
    product_id = SelectField('Product', coerce=int, validators=[DataRequired()], choices=[])
    quantity = DecimalField('Quantity', validators=[DataRequired()], places=3, default=1)
    # These fields will be auto-populated from selected product
    product_name = HiddenField()
    description = HiddenField()
    hsn_code = HiddenField()
    unit = HiddenField()
    rate = HiddenField()
    gst_rate = HiddenField()

class BillForm(FlaskForm):
    customer_id = SelectField('Customer', coerce=int, validators=[DataRequired()])
    bill_date = DateField('Bill Date', validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[Optional()])
    status = SelectField('Status', validators=[DataRequired()], choices=[
        ('Draft', 'Draft'),
        ('Sent', 'Sent'),
        ('Paid', 'Paid'),
        ('Cancelled', 'Cancelled')
    ], default='Draft')
    discount_type = SelectField('Discount Type', choices=[
        ('none', 'No Discount'),
        ('percentage', 'Percentage (%)'),
        ('amount', 'Fixed Amount (₹)')
    ], default='none')
    discount_value = DecimalField('Discount Value', validators=[Optional()], places=2, default=0)
    notes = TextAreaField('Notes', validators=[Optional()])
    items = FieldList(FormField(BillItemForm), min_entries=1)

# Authentication Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[Optional(), Length(max=100)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=100)])
    phone = StringField('Phone', validators=[Optional(), Length(max=15)])
    role = SelectField('Role', validators=[DataRequired()], choices=[
        ('user', 'User'),
        ('manager', 'Manager'),
        ('admin', 'Administrator')
    ])
    is_active = BooleanField('Active User', default=True)
    password = PasswordField('Password', validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[Optional(), EqualTo('password', message='Passwords must match')])

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', 
                                   validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')])

class CreateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[Optional(), Length(max=100)])
    last_name = StringField('Last Name', validators=[Optional(), Length(max=100)])
    phone = StringField('Phone', validators=[Optional(), Length(max=15)])
    role = SelectField('Role', validators=[DataRequired()], choices=[
        ('user', 'User'),
        ('manager', 'Manager'),
        ('admin', 'Administrator')
    ])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

class CategoryForm(FlaskForm):
    category_name = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=100)])

class FieldDefinitionForm(FlaskForm):
    entity_type = SelectField('Entity Type', validators=[DataRequired()], choices=[
        ('product', 'Product'),
        ('customer', 'Customer'),
        ('bill', 'Bill')
    ])
    field_name = StringField('Field Name', validators=[
        DataRequired(), 
        Length(min=2, max=50),
        Regexp(r'^[a-z][a-z0-9_]*$', message='Field name must start with a lowercase letter and contain only lowercase letters, numbers, and underscores')
    ])
    display_name = StringField('Display Name', validators=[DataRequired(), Length(min=2, max=100)])
    field_type = SelectField('Field Type', validators=[DataRequired()], choices=[
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('boolean', 'Boolean'),
        ('select', 'Select')
    ])
    field_order = IntegerField('Display Order', default=0, validators=[NumberRange(min=0)])
    required = BooleanField('Required Field')
    searchable = BooleanField('Searchable', description='Enable this for barcode or serial number fields that should be searchable')
    enabled = BooleanField('Enabled', default=True)
    options = TextAreaField('Options (one per line)', validators=[Optional()])
    validation_regex = StringField('Validation Pattern', validators=[Optional()])
    help_text = TextAreaField('Help Text', validators=[Optional()])
