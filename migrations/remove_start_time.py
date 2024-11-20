import os
import sys
from sqlalchemy import text

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Todo

def remove_start_time():
    with app.app_context():
        # Drop the start_time column
        with db.engine.connect() as conn:
            conn.execute(text('ALTER TABLE todo DROP COLUMN start_time'))
            conn.commit()

if __name__ == '__main__':
    remove_start_time()
