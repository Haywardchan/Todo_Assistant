from app import app, db, Todo

def migrate_database():
    with app.app_context():
        # Add parent_group column if it doesn't exist
        try:
            db.session.execute('ALTER TABLE todo ADD COLUMN parent_group VARCHAR(50)')
            db.session.commit()
            print("Successfully added parent_group column")
        except Exception as e:
            print(f"Column might already exist or other error occurred: {e}")
            db.session.rollback()

if __name__ == '__main__':
    migrate_database()
