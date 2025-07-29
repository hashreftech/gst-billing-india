from app import app
from app import db
from field_utils import initialize_default_fields

if __name__ == '__main__':
    # Initialize custom fields on application startup
    with app.app_context():
        initialize_default_fields()
    
    # Run the application on port 5001 to avoid conflicts with system services
    app.run(host='0.0.0.0', port=5001, debug=True)
