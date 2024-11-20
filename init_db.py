import os
from app import app, db

# Delete existing database
db_path = os.path.join(app.instance_path, 'todos.db')
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Deleted existing database: {db_path}")

# Create new database with updated schema
with app.app_context():
    db.create_all()
    print("Created new database with updated schema")
