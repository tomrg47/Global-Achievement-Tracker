from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    with db.engine.connect() as connection:
        # Allow email to be NULL
        connection.execute(text("ALTER TABLE users ALTER COLUMN email DROP NOT NULL;"))
        
        # Allow password_hash to be NULL (since Steam users won't have a password initially)
        connection.execute(text("ALTER TABLE users ALTER COLUMN password_hash DROP NOT NULL;"))
        
        connection.commit()
        print("Database schema updated: email and password_hash columns are now nullable.")
