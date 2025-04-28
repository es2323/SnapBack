import sqlite3

def setup_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        name TEXT,
        role TEXT CHECK(role IN ('employee', 'manager', 'hr')) NOT NULL,
        team TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS game_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        game_type TEXT,
        fatigue_score INTEGER,
        reaction_time INTEGER,
        accuracy INTEGER,
        errors INTEGER,
        completion_time INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_email) REFERENCES users(email)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS check_ins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        rest_score INTEGER,
        discomfort TEXT,
        notes TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_email) REFERENCES users(email)
    )
    ''')

    # Seed initial users
    users = [
        ("levi@example.com", "pass123", "Levi", "employee", "Team A"),
        ("manager1@example.com", "managerpass", "Sarah", "manager", "Team A"),
        ("hr@example.com", "hrpass", "Alex", "hr", "HR")
    ]

    for user in users:
        cursor.execute(
            "INSERT OR IGNORE INTO users (email, password, name, role, team) VALUES (?, ?, ?, ?, ?)",
            user
        )

    conn.commit()
    conn.close()
    print("✅ Database setup complete.")

if __name__ == "__main__":
    setup_database()
