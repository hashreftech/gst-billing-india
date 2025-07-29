#!/bin/bash
# Script to reset the database and initialize it with default data

echo "GST Billing System - Database Reset and Initialization"
echo "====================================================="

# Check if the virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Activating virtual environment..."
    if [ -d "venv" ]; then
        source venv/bin/activate
    elif [ -d ".venv" ]; then
        source .venv/bin/activate
    else
        echo "Error: Virtual environment not found. Please create it first."
        exit 1
    fi
fi

# Determine Python command
PYTHON_CMD="python"
if ! command -v $PYTHON_CMD &> /dev/null; then
    PYTHON_CMD="python3"
    if ! command -v $PYTHON_CMD &> /dev/null; then
        PYTHON_CMD="python3.11"
        if ! command -v $PYTHON_CMD &> /dev/null; then
            echo "Error: Could not find Python. Please ensure Python is installed."
            exit 1
        fi
    fi
fi

# Check for required packages
echo "Checking for required packages..."
$PYTHON_CMD -c "import dotenv" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Installing python-dotenv..."
    pip install python-dotenv
fi

$PYTHON_CMD -c "import sqlalchemy" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Installing sqlalchemy..."
    pip install sqlalchemy
fi

echo "Step 1: Resetting the database..."
$PYTHON_CMD db_manage.py reset

if [ $? -ne 0 ]; then
    echo "Error: Database reset failed. Aborting."
    exit 1
fi

echo "Step 2: Initializing database with default data..."
$PYTHON_CMD initialize_defaults.py

if [ $? -ne 0 ]; then
    echo "Error: Database initialization failed."
    exit 1
fi

echo "Database reset and initialization completed successfully!"
echo "You can now login with username 'admin' and password 'admin123'"
