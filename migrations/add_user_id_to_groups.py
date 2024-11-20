"""Add user_id to groups

This migration adds a user_id column to the groups table and associates existing groups
with the first user in the database.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Group, User
from sqlalchemy import text

def upgrade():
    with app.app_context():
        # Create a new table with the user_id column
        with db.engine.connect() as conn:
            # Create new table
            conn.execute(text('''
                CREATE TABLE group_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(50) NOT NULL,
                    parent_group VARCHAR(50),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER NOT NULL REFERENCES user(id)
                )
            '''))
            
            # Get the first user (or create one if none exists)
            user = User.query.first()
            if user:
                # Copy data to new table with user_id
                conn.execute(text(f'''
                    INSERT INTO group_new (id, name, parent_group, created_at, user_id)
                    SELECT id, name, parent_group, created_at, {user.id}
                    FROM "group"
                '''))
            
            # Drop old table and rename new table
            conn.execute(text('DROP TABLE "group"'))
            conn.execute(text('ALTER TABLE group_new RENAME TO "group"'))
            
            conn.commit()

def downgrade():
    with app.app_context():
        # Create a new table without user_id
        with db.engine.connect() as conn:
            conn.execute(text('''
                CREATE TABLE group_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(50) NOT NULL,
                    parent_group VARCHAR(50),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            '''))
            
            # Copy data to new table without user_id
            conn.execute(text('''
                INSERT INTO group_new (id, name, parent_group, created_at)
                SELECT id, name, parent_group, created_at
                FROM "group"
            '''))
            
            # Drop old table and rename new table
            conn.execute(text('DROP TABLE "group"'))
            conn.execute(text('ALTER TABLE group_new RENAME TO "group"'))
            
            conn.commit()

if __name__ == '__main__':
    upgrade()
