from app.services.db_service import get_db_connection


def create_tables():
    db = get_db_connection()
    cursor = db.cursor()

    # -----------------------------------
    # Users Table
    # -----------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            mobile TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # -----------------------------------
    # Reports Table
    # -----------------------------------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            issue TEXT NOT NULL,
            location TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            users_id INTEGER,
            mobile TEXT NOT NULL,
            priority TEXT,
            confidence REAL,
            assigned_to TEXT,
            proof_file TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (users_id)
            REFERENCES users(id)
        )
    """)

    db.commit()
    cursor.close()
    db.close()

    print("Database created successfully")


if __name__ == "__main__":
    create_tables()