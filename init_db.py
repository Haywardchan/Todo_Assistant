from flask import Flask
from models import db, User, Group, Todo
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_app():
    # Create a minimal Flask application
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True  # Enable SQL logging
    
    # Initialize the database
    db.init_app(app)
    return app

def init_db():
    app = create_app()
    
    # Delete existing database
    db_path = os.path.join(app.instance_path, 'todos.db')
    if os.path.exists(db_path):
        os.remove(db_path)
        logger.info(f"Deleted existing database: {db_path}")

    # Ensure instance folder exists
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)
        logger.info(f"Created instance directory: {app.instance_path}")

    with app.app_context():
        # Verify models are registered
        logger.info("Registered models:")
        for table in db.metadata.tables.keys():
            logger.info(f"- {table}")
        
        # Create tables
        db.create_all()
        logger.info("Created database schema")
        
        # Verify tables were created
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        required_tables = {'user', 'group', 'todo'}
        
        if not all(table in tables for table in required_tables):
            logger.warning("Not all required tables exist. Recreating tables...")
            db.drop_all()
            db.create_all()
        
        # Log created tables and their structure
        logger.info("Created tables:")
        for table in inspector.get_table_names():
            logger.info(f"- {table}")
            logger.info(f"  Columns: {[col['name'] for col in inspector.get_columns(table)]}")

if __name__ == '__main__':
    init_db()
