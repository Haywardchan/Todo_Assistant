#!/bin/bash

# Create instance directory if it doesn't exist
mkdir -p instance

# Set environment variables for development if not set
if [ -z "$GOOGLE_CLIENT_ID" ]; then
    echo "Setting development environment variables..."
    export GOOGLE_CLIENT_ID="dummy-client-id"
    export FLASK_SECRET_KEY="development-secret-key"
fi

# Initialize the database
echo "Initializing database..."
python init_db.py 2>&1 | tee db_init.log
if [ $? -ne 0 ]; then
    echo "Failed to initialize database. Check db_init.log for details"
    cat db_init.log
    exit 1
fi

# Verify database was created
if [ ! -f instance/todos.db ]; then
    echo "Error: Database file was not created"
    exit 1
fi

# List database files
echo "Database files:"
ls -l instance/

# Check database schema
echo "Database schema:"
sqlite3 instance/todos.db ".schema"

# Start the application
echo "Starting application..."
gunicorn app:app --bind 0.0.0.0:5000
