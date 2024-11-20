#!/bin/bash

# Create instance directory if it doesn't exist
mkdir -p instance

# Set proper permissions
chmod 777 instance

# Initialize the database
echo "Initializing database..."
python init_db.py
if [ $? -ne 0 ]; then
    echo "Failed to initialize database"
    exit 1
fi

# Start the application
echo "Starting application..."
gunicorn app:app --bind 0.0.0.0:5000
