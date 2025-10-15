import sqlite3

conn = sqlite3.connect("cooknet.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    name TEXT,
    description TEXT
)
""")
conn.commit()
conn.close()
