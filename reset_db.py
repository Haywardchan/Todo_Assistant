from app import app, db, Todo, Group
import os

def reset_database():
    # Get the path to the database file
    db_path = os.path.join(app.instance_path, 'todos.db')
    
    # Remove the existing database file
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Removed existing database: {db_path}")
    
    # Create the instance folder if it doesn't exist
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
        print(f"Created instance folder: {app.instance_path}")
    
    # Create all tables
    with app.app_context():
        db.create_all()
        print("Created new database with all tables")

if __name__ == '__main__':
    reset_database()
