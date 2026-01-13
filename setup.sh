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

# Check for .env file first (needed for database connection)
echo -e "\n${YELLOW}Checking for .env file...${NC}"
if [ -f ".env" ]; then
    echo -e "${GREEN}✓ .env file exists${NC}"
    
    # Load DATABASE_URL from .env
    export $(grep -v '^#' .env | grep DATABASE_URL | xargs)
    
    # Test PostgreSQL connection
    echo -e "\n${YELLOW}Testing PostgreSQL connection...${NC}"
    if [ -z "$DATABASE_URL" ]; then
        echo -e "${RED}✗ DATABASE_URL not found in .env file${NC}"
        exit 1
    fi
    
    # Extract connection details using Python (more reliable than sed for URL parsing)
    DB_DETAILS=$(python3 -c "
from urllib.parse import urlparse
import sys
try:
    result = urlparse('$DATABASE_URL')
    print(f'{result.hostname}|{result.port}|{result.username}|{result.password}|{result.path[1:]}')
except Exception as e:
    print('ERROR', file=sys.stderr)
    sys.exit(1)
")
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Failed to parse DATABASE_URL${NC}"
        exit 1
    fi
    
    IFS='|' read -r DB_HOST DB_PORT DB_USER DB_PASS DB_NAME <<< "$DB_DETAILS"
    
    echo -e "${YELLOW}Connecting to PostgreSQL at $DB_HOST:$DB_PORT...${NC}"
    
    # Test connection using psql (if available) or python
    if command -v psql &>/dev/null; then
        if PGPASSWORD="$DB_PASS" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1;" &>/dev/null 2>&1; then
            echo -e "${GREEN}✓ PostgreSQL connection successful${NC}"
        else
            echo -e "${RED}✗ Failed to connect to PostgreSQL${NC}"
            echo -e "${YELLOW}! Please verify your DATABASE_URL in .env file${NC}"
            echo -e "${YELLOW}! Database: $DB_NAME, User: $DB_USER, Host: $DB_HOST:$DB_PORT${NC}"
            echo -e "${YELLOW}! Ensure the remote PostgreSQL server is accessible${NC}"
            exit 1
        fi
    else
        # Fallback: test connection using Python
        echo -e "${YELLOW}Testing connection using Python...${NC}"
        python3 -c "
import sys
try:
    import psycopg2
    conn = psycopg2.connect('$DATABASE_URL')
    conn.close()
    print('✓ PostgreSQL connection successful')
    sys.exit(0)
except ImportError:
    print('! psycopg2 not installed yet, will verify after installing dependencies')
    sys.exit(0)
except Exception as e:
    print(f'✗ Failed to connect to PostgreSQL: {e}')
    sys.exit(1)
" || exit 1
    fi
else
    echo -e "${YELLOW}! .env file not found. It will be created with sample configuration.${NC}"
    echo -e "${YELLOW}! You must update it with your remote PostgreSQL credentials before running the application.${NC}"
fi

# Set up virtual environment
echo -e "\n${YELLOW}Setting up virtual environment...${NC}"
if [ -f "venv/bin/activate" ]; then
    echo -e "${YELLOW}Virtual environment already exists.${NC}"
elif [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment directory exists but is missing activation script. Recreating...${NC}"
    rm -rf venv
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "\n${YELLOW}Activating virtual environment...${NC}"
if [ -f "venv/bin/activate" ]; then
    # shellcheck disable=SC1091
    . venv/bin/activate
    echo -e "${GREEN}✓ Virtual environment activated${NC}"
else
    echo -e "${RED}✗ Failed to activate virtual environment (venv/bin/activate missing)${NC}"
    echo -e "${YELLOW}! Recreate venv or check permissions${NC}"
    exit 1
fi

# Install dependencies
echo -e "\n${YELLOW}Installing dependencies...${NC}"
python3 -m pip install --upgrade pip
if ! python3 -m pip install -r requirements.txt; then
    echo -e "${YELLOW}! Some dependencies failed to install. Attempting fallbacks where possible.${NC}"
fi
echo -e "${GREEN}✓ Dependencies install step completed${NC}"

# Verify database connection after installing dependencies
if [ -f ".env" ]; then
    echo -e "\n${YELLOW}Verifying database connection with installed dependencies...${NC}"
    export $(grep -v '^#' .env | grep DATABASE_URL | xargs)

    # Ensure psycopg2 is available; if not, install psycopg2-binary
    python3 -c "import importlib.util, sys; sys.exit(0) if importlib.util.find_spec('psycopg2') else sys.exit(2)"
    if [ $? -eq 2 ]; then
        echo -e "${YELLOW}psycopg2 not found; installing psycopg2-binary...${NC}"
        python3 -m pip install psycopg2-binary
    fi

    # Verify actual connection
    python3 -c "
import sys
try:
    import psycopg2
    conn = psycopg2.connect('$DATABASE_URL')
    conn.close()
    print('✓ Database connection verified successfully')
    sys.exit(0)
except Exception as e:
    print(f'✗ Failed to connect to PostgreSQL: {e}')
    print('! Please verify your DATABASE_URL in .env file')
    print('! Ensure the remote PostgreSQL server is accessible')
    sys.exit(1)
" || exit 1
fi

# Check for .env file
echo -e "\n${YELLOW}Checking .env configuration...${NC}"
if [ -f ".env" ]; then
    echo -e "${GREEN}✓ .env file is configured${NC}"
else
    echo -e "${YELLOW}Creating sample .env file...${NC}"
    cat > .env << EOF
# Database Configuration
# Update this with your remote PostgreSQL server details
DATABASE_URL=postgresql://username:password@your-db-host:5432/database_name

# Session Secret (generate a random string - required for authentication)
SESSION_SECRET=$(python3 -c 'import secrets; print(secrets.token_hex(32))')

# Flask Environment
FLASK_ENV=development
FLASK_DEBUG=True
EOF
    echo -e "${GREEN}✓ Sample .env file created${NC}"
    echo -e "${RED}!!! IMPORTANT: Edit the .env file with your remote PostgreSQL server credentials !!!${NC}"
    echo -e "${YELLOW}! Update DATABASE_URL with: postgresql://user:password@host:port/database${NC}"
    exit 1
fi

# Skip local database creation since using remote PostgreSQL

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
        venv/bin/python db_manage.py init
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
            venv/bin/python db_manage.py reset
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
        venv/bin/python db_manage.py upgrade
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
