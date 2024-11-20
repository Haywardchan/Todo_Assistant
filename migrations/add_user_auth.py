"""Add user authentication

This migration adds the User table and adds a user_id column to the Todo table.
"""

import sqlite3
import os

def upgrade():
    # Make sure the instance directory exists
    os.makedirs('instance', exist_ok=True)
    
    conn = sqlite3.connect('instance/todos.db')
    cursor = conn.cursor()

    # Create user table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email VARCHAR(100) UNIQUE NOT NULL,
            name VARCHAR(100)
        )
    ''')

    # Create a default user for existing todos
    cursor.execute('''
        INSERT INTO user (email, name)
        VALUES ('default@example.com', 'Default User')
    ''')
    default_user_id = cursor.lastrowid

    # Add user_id column to todo table
    try:
        cursor.execute('ALTER TABLE todo ADD COLUMN user_id INTEGER REFERENCES user(id)')
    except sqlite3.OperationalError:
        # Column might already exist
        pass

    # Update existing todos to belong to the default user
    cursor.execute('UPDATE todo SET user_id = ? WHERE user_id IS NULL', (default_user_id,))

    conn.commit()
    conn.close()

def downgrade():
    conn = sqlite3.connect('instance/todos.db')
    cursor = conn.cursor()

    # Remove the user_id column from todo table and the user table
    cursor.execute('DROP TABLE IF EXISTS user')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    upgrade()
