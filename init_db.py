from flask import Flask
from models import db, User, Group, Todo
import os

# Create a minimal Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Delete existing database
db_path = os.path.join(app.instance_path, 'todos.db')
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Deleted existing database: {db_path}")

# Ensure instance folder exists
if not os.path.exists(app.instance_path):
    os.makedirs(app.instance_path)

# Create new database with updated schema
with app.app_context():
    db.create_all()
    print("Created new database with updated schema")
