from flask import Flask
from models import db, User, Group, Todo
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create a minimal Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Enable SQL logging

# Initialize the database
db.init_app(app)

# Delete existing database
db_path = os.path.join(app.instance_path, 'todos.db')
if os.path.exists(db_path):
    os.remove(db_path)
    logger.info(f"Deleted existing database: {db_path}")

# Ensure instance folder exists
if not os.path.exists(app.instance_path):
    os.makedirs(app.instance_path)
    logger.info(f"Created instance directory: {app.instance_path}")

# Create new database with updated schema
with app.app_context():
    # Verify models are registered
    logger.info("Registered models:")
    for table in db.metadata.tables.keys():
        logger.info(f"- {table}")
    
    # Create tables
    db.create_all()
    logger.info("Created new database with updated schema")
    
    # Verify tables were created
    engine = db.engine
    inspector = db.inspect(engine)
    logger.info("Created tables:")
    for table in inspector.get_table_names():
        logger.info(f"- {table}")
        logger.info(f"  Columns: {[col['name'] for col in inspector.get_columns(table)]}")
