#!/bin/bash

# Initialize the database
python init_db.py

# Start the application
gunicorn app:app --bind 0.0.0.0:5000
