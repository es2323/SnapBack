import sqlite3

conn = sqlite3.connect('main.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT,
    name TEXT,
    role TEXT CHECK(role IN ('employee', 'manager')) NOT NULL
)
''')

users = [
    ("test@example.com", "test123", "Test User", "employee"),
    ("manager@example.com", "admin123", "Manager One", "manager")
]

for user in users:
    cursor.execute("INSERT OR IGNORE INTO users (email, password, name, role) VALUES (?, ?, ?, ?)", user)

conn.commit()
conn.close()
print("✅ Database created and seeded.")
