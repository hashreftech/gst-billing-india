#!/usr/bin/env bash
# Setup script for the GST Billing Software

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}GST Billing Software - Setup Script${NC}"
echo -e "${YELLOW}======================================${NC}"

# Check if Python is installed
echo -e "\n${YELLOW}Checking Python installation...${NC}"
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Python is installed: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python 3 is not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

# Check if PostgreSQL is installed
echo -e "\n${YELLOW}Checking PostgreSQL installation...${NC}"
if command -v psql &>/dev/null; then
    PSQL_VERSION=$(psql --version)
    echo -e "${GREEN}✓ PostgreSQL is installed: $PSQL_VERSION${NC}"
else
    echo -e "${RED}✗ PostgreSQL is not installed. Please install PostgreSQL.${NC}"
    exit 1
fi

# Set up virtual environment
echo -e "\n${YELLOW}Setting up virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists. Skipping creation.${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "\n${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install dependencies
echo -e "\n${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Check for .env file
echo -e "\n${YELLOW}Checking for .env file...${NC}"
if [ -f ".env" ]; then
    echo -e "${GREEN}✓ .env file exists${NC}"
else
    echo -e "${YELLOW}Creating sample .env file...${NC}"
    cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/gst_billing_db

# Session Secret (generate a random string - required for authentication)
SESSION_SECRET=$(python3 -c 'import secrets; print(secrets.token_hex(32))')

# Flask Environment
FLASK_ENV=development
FLASK_DEBUG=True
EOF
    echo -e "${GREEN}✓ Sample .env file created${NC}"
    echo -e "${YELLOW}! Please edit the .env file with your actual database credentials${NC}"
fi

# Ask if user wants to create the database
echo -e "\n${YELLOW}Do you want to create the PostgreSQL database? (y/n)${NC}"
read -r create_db
if [[ $create_db =~ ^[Yy]$ ]]; then
    echo -e "\n${YELLOW}Enter database name (default: gst_billing_db):${NC}"
    read -r db_name
    db_name=${db_name:-gst_billing_db}
    
    echo -e "\n${YELLOW}Creating database $db_name...${NC}"
    if createdb "$db_name"; then
        echo -e "${GREEN}✓ Database $db_name created${NC}"
        
        # Update .env file with the correct database name
        sed -i.bak "s/gst_billing_db/$db_name/g" .env
        rm .env.bak
    else
        echo -e "${RED}✗ Failed to create database $db_name${NC}"
        echo -e "${YELLOW}! You'll need to create the database manually${NC}"
    fi
fi

# Ask about database operations
echo -e "\n${YELLOW}Database Operations:${NC}"
echo -e "1. Initialize database (first-time setup)"
echo -e "2. Reset database (WARNING: This will delete all data)"
echo -e "3. Upgrade database to latest migration"
echo -e "4. Skip database operations"
echo -e "\n${YELLOW}Choose an option (1-4):${NC}"
read -r db_operation

case $db_operation in
    1)
        echo -e "\n${YELLOW}Initializing database...${NC}"
        python3 db_manage.py init
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ Database initialized successfully${NC}"
        else
            echo -e "${RED}✗ Error initializing database${NC}"
            echo -e "${YELLOW}! Check the error messages above and fix any issues${NC}"
        fi
        ;;
    2)
        echo -e "\n${RED}WARNING: This will delete all data in the database.${NC}"
        echo -e "${YELLOW}Are you sure you want to continue? (y/n)${NC}"
        read -r confirm_reset
        if [[ $confirm_reset =~ ^[Yy]$ ]]; then
            echo -e "\n${YELLOW}Resetting database...${NC}"
            python3 db_manage.py reset
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}✓ Database reset successfully${NC}"
            else
                echo -e "${RED}✗ Error resetting database${NC}"
                echo -e "${YELLOW}! Check the error messages above and fix any issues${NC}"
            fi
        else
            echo -e "${YELLOW}Database reset cancelled.${NC}"
        fi
        ;;
    3)
        echo -e "\n${YELLOW}Upgrading database...${NC}"
        python3 db_manage.py upgrade
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ Database upgraded successfully${NC}"
        else
            echo -e "${RED}✗ Error upgrading database${NC}"
            echo -e "${YELLOW}! Check the error messages above and fix any issues${NC}"
        fi
        ;;
    4)
        echo -e "${YELLOW}Skipping database operations.${NC}"
        ;;
    *)
        echo -e "${RED}Invalid option. Skipping database operations.${NC}"
        ;;
esac

# Create uploads directory
echo -e "\n${YELLOW}Creating uploads directory...${NC}"
mkdir -p uploads
echo -e "${GREEN}✓ Uploads directory created${NC}"

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Setup completed!${NC}"
echo -e "${YELLOW}To start the application, run:${NC}"
echo -e "source venv/bin/activate"
echo -e "python3 app.py"
echo -e "\n${YELLOW}Default login:${NC}"
echo -e "Username: admin"
echo -e "Password: admin123"
echo -e "${RED}!!! IMPORTANT: Change the default password after first login !!!${NC}"
echo -e "${GREEN}========================================${NC}"
