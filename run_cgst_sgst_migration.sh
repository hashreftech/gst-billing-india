#!/bin/bash
# Script to run the database migration

echo "GST Billing System Database Migration Script"
echo "==========================================="

# Check if DATABASE_URL is already set in environment
if [ -z "$DATABASE_URL" ]; then
    echo "DATABASE_URL environment variable not found."
    
    # Ask user for database connection details
    read -p "Enter database name [softwareindia]: " dbname
    dbname=${dbname:-softwareindia}
    
    read -p "Enter database user [postgres]: " dbuser
    dbuser=${dbuser:-postgres}
    
    read -s -p "Enter database password [postgres]: " dbpass
    dbpass=${dbpass:-postgres}
    echo ""
    
    read -p "Enter database host [localhost]: " dbhost
    dbhost=${dbhost:-localhost}
    
    read -p "Enter database port [5432]: " dbport
    dbport=${dbport:-5432}
    
    # Set DATABASE_URL
    export DATABASE_URL="postgresql://$dbuser:$dbpass@$dbhost:$dbport/$dbname"
    echo "Set DATABASE_URL to postgresql://$dbuser:****@$dbhost:$dbport/$dbname"
else
    echo "Using existing DATABASE_URL from environment."
fi

# Try to install required packages
echo "Checking for required packages..."
pip install psycopg2-binary python-dotenv

# Run the migration script
echo "Running migration script..."
python migrations/direct_migration.py

# Check exit status
if [ $? -eq 0 ]; then
    echo "Migration completed successfully!"
else
    echo "Migration failed. Check the error messages above."
    exit 1
fi
