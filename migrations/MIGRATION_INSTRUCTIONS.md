# Database Migration Instructions

This document provides instructions for adding the CGST and SGST rate columns to your database tables.

## Option 1: Run using the app's database connection

This is the preferred method as it uses the app's existing database connection:

```bash
# Navigate to the project root directory
cd /Users/mathanrajkrishnan/Projects/Billing/SoftwareIndiaGst

# Run the migration script
python migrations/run_migration.py
```

## Option 2: Run the direct database migration script

If Option 1 doesn't work due to import issues, you can try this method:

```bash
# Install required packages if not already installed
pip install psycopg2-binary python-dotenv

# Navigate to the project root directory
cd /Users/mathanrajkrishnan/Projects/Billing/SoftwareIndiaGst

# Run the direct migration script
python migrations/direct_migration.py
```

## Option 3: Run the SQL directly using psql

If both Python methods fail, you can run the SQL directly with psql:

```bash
# Navigate to the project root directory
cd /Users/mathanrajkrishnan/Projects/Billing/SoftwareIndiaGst

# Run the SQL script (replace with your actual database credentials)
psql -U your_username -d your_database_name -f migrations/add_cgst_sgst_columns.sql
```

## Option 4: Execute SQL statements manually

If none of the above methods work, you can copy and paste the SQL statements directly into your PostgreSQL client:

1. Open your PostgreSQL client (psql, pgAdmin, etc.)
2. Connect to your database
3. Open the file `/Users/mathanrajkrishnan/Projects/Billing/SoftwareIndiaGst/migrations/add_cgst_sgst_columns.sql`
4. Copy and paste the SQL statements into your database client and execute them

## Verifying the Migration

After running the migration, you can verify that the columns were added successfully:

```sql
-- Check if the columns exist in the product table
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'product' AND column_name IN ('cgst_rate', 'sgst_rate');

-- Check if the columns exist in the bill_item table
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'bill_item' AND column_name IN ('cgst_rate', 'sgst_rate');
```

## Troubleshooting

If you encounter any issues:

1. Check your database connection details
2. Ensure you have the necessary permissions to alter tables
3. Verify that the product and bill_item tables exist in your database
4. Check for any error messages in the output
