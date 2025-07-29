# Database Migration Management

## Overview
The application uses Alembic for database migrations, which allows for versioned database schema changes. This enables:
- Tracking all database schema changes in version control
- Upgrading or downgrading database schema to specific versions
- Resetting the database to a clean state without losing schema information

## Migration Commands

The `db_manage.py` script provides several commands for managing the database:

### Initialize Database (First-time Setup)
```bash
python3 db_manage.py init
```
This creates all tables and initial data based on the latest migration version.

### Reset Database (Delete All Data and Recreate Schema)
```bash
python3 db_manage.py reset
```
This drops all tables and recreates them, effectively resetting the database to a clean state.
**WARNING**: This operation deletes all data in the database.

### Upgrade Database (Apply Pending Migrations)
```bash
python3 db_manage.py upgrade
```
This applies any unapplied migrations to bring the database schema up to date.

### Downgrade Database (Revert Migrations)
```bash
python3 db_manage.py downgrade [revision]
```
This downgrades the database schema to a specific revision.

### Create a New Migration
```bash
python3 db_manage.py revision --message "Description of the change"
```
This creates a new migration file in the `alembic/versions` directory.

## Migration File Structure
Migration files are stored in the `alembic/versions` directory and follow a standard format:
- Each file has an upgrade() function that applies changes
- Each file has a downgrade() function that reverts changes
- Files are named with a timestamp and description for easy tracking

## Example: Adding a New Field
To add a new field to an existing table:

1. Create a new migration:
```bash
python3 db_manage.py revision --message "Add phone_verified field to users"
```

2. Edit the generated migration file to define the upgrade and downgrade operations:
```python
def upgrade():
    op.add_column('users', sa.Column('phone_verified', sa.Boolean(), nullable=False, server_default='false'))

def downgrade():
    op.drop_column('users', 'phone_verified')
```

3. Apply the migration:
```bash
python3 db_manage.py upgrade
```

This approach ensures that all database changes are tracked, reproducible, and can be reverted if needed.
