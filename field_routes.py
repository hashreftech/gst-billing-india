"""
Routes for managing custom fields in the application.

This module provides routes for administrators to create, edit, and manage
custom fields for different entity types (products, customers, etc.).
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import app, db
from models import FieldDefinition, FieldData
from forms import FieldDefinitionForm
from field_utils import (
    get_entity_field_value, set_entity_field_value,
    create_field_definition, update_field_definition, delete_field_definition
)
import json

# Create a Blueprint for field management routes
field_bp = Blueprint('fields', __name__)

@field_bp.route('/settings/fields')
@login_required
def field_management():
    """Field management main page"""
    if not current_user.is_admin():
        flash('You do not have permission to access field settings.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get entity types with fields
    entity_types = db.session.query(FieldDefinition.entity_type).distinct().all()
    entity_types = [et[0] for et in entity_types]
    
    # Default to 'product' if available, otherwise first entity type
    selected_type = request.args.get('type', 'product' if 'product' in entity_types else entity_types[0] if entity_types else None)
    
    # Get fields for selected type
    fields = []
    if selected_type:
        fields = FieldDefinition.query.filter_by(entity_type=selected_type).order_by(FieldDefinition.field_order).all()
    
    return render_template(
        'settings/field_management.html',
        entity_types=entity_types,
        selected_type=selected_type,
        fields=fields
    )

@field_bp.route('/settings/fields/new', methods=['GET', 'POST'])
@login_required
def new_field():
    """Create a new custom field"""
    if not current_user.is_admin():
        flash('You do not have permission to create fields.', 'danger')
        return redirect(url_for('dashboard'))
    
    form = FieldDefinitionForm()
    
    if form.validate_on_submit():
        # Get options for select fields
        options = None
        if form.field_type.data == 'select':
            options_text = form.options.data
            options = [opt.strip() for opt in options_text.split('\n') if opt.strip()]
        
        # Create the field definition
        field_def = create_field_definition(
            entity_type=form.entity_type.data,
            field_name=form.field_name.data,
            display_name=form.display_name.data,
            field_type=form.field_type.data,
            required=form.required.data,
            enabled=form.enabled.data,
            field_order=form.field_order.data,
            options=options,
            help_text=form.help_text.data,
            validation_regex=form.validation_regex.data,
            user_id=current_user.id
        )
        
        if field_def:
            flash(f'Field "{form.display_name.data}" created successfully.', 'success')
            return redirect(url_for('fields.field_management', type=form.entity_type.data))
        else:
            flash('Failed to create field. Please check your inputs.', 'danger')
    
    # For GET request or failed POST
    return render_template(
        'settings/field_form.html',
        form=form,
        field=None,
        action='create'
    )

@field_bp.route('/settings/fields/edit/<int:field_id>', methods=['GET', 'POST'])
@login_required
def edit_field(field_id):
    """Edit an existing custom field"""
    if not current_user.is_admin():
        flash('You do not have permission to edit fields.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get the field definition
    field = FieldDefinition.query.get_or_404(field_id)
    
    # Create form and populate with field data
    form = FieldDefinitionForm(obj=field)
    
    # For select fields, convert options from JSON to newline-separated text
    options_text = ""
    if field.options:
        try:
            options = json.loads(field.options)
            options_text = "\n".join(options)
            form.options.data = options_text
        except:
            pass
    
    if form.validate_on_submit():
        # Get options for select fields
        options = None
        if form.field_type.data == 'select':
            options_text = form.options.data
            options = [opt.strip() for opt in options_text.split('\n') if opt.strip()]
        
        # Update the field definition
        updated_field = update_field_definition(
            field_id=field_id,
            display_name=form.display_name.data,
            field_type=form.field_type.data,
            required=form.required.data,
            enabled=form.enabled.data,
            field_order=form.field_order.data,
            options=options,
            help_text=form.help_text.data,
            validation_regex=form.validation_regex.data,
            user_id=current_user.id
        )
        
        if updated_field:
            flash(f'Field "{form.display_name.data}" updated successfully.', 'success')
            return redirect(url_for('fields.field_management', type=field.entity_type))
        else:
            flash('Failed to update field. Please check your inputs.', 'danger')
    
    # For GET request or failed POST
    return render_template(
        'settings/field_form.html',
        form=form,
        field=field,
        options=options_text,
        action='edit'
    )

@field_bp.route('/settings/fields/delete/<int:field_id>', methods=['POST'])
@login_required
def delete_field(field_id):
    """Delete a custom field"""
    if not current_user.is_admin():
        flash('You do not have permission to delete fields.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Get the field definition
    field = FieldDefinition.query.get_or_404(field_id)
    entity_type = field.entity_type
    
    # Delete the field
    if delete_field_definition(field_id, user_id=current_user.id):
        flash(f'Field "{field.display_name}" deleted successfully.', 'success')
    else:
        flash(f'Failed to delete field "{field.display_name}".', 'danger')
    
    return redirect(url_for('fields.field_management', type=entity_type))

@field_bp.route('/settings/fields/toggle/<int:field_id>', methods=['POST'])
@login_required
def toggle_field(field_id):
    """Toggle a field's enabled status"""
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    # Get the field definition
    field = FieldDefinition.query.get_or_404(field_id)
    
    # Toggle the enabled status
    updated_field = update_field_definition(
        field_id=field_id,
        enabled=not field.enabled,
        user_id=current_user.id
    )
    
    if updated_field:
        return jsonify({
            'success': True, 
            'enabled': updated_field.enabled,
            'message': f'Field "{updated_field.display_name}" {"enabled" if updated_field.enabled else "disabled"}'
        })
    else:
        return jsonify({'success': False, 'message': 'Failed to update field'}), 500

@field_bp.route('/settings/fields/reorder', methods=['POST'])
@login_required
def reorder_fields():
    """Reorder fields"""
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    try:
        # Get the field IDs in the new order
        field_ids = request.json.get('field_ids', [])
        
        # Update the field order
        for index, field_id in enumerate(field_ids):
            update_field_definition(
                field_id=int(field_id),
                field_order=index,
                user_id=current_user.id
            )
        
        return jsonify({'success': True, 'message': 'Fields reordered successfully'})
    except Exception as e:
        app.logger.error(f"Error reordering fields: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to reorder fields'}), 500

# Register the blueprint with the application
app.register_blueprint(field_bp)
