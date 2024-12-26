import sqlite3

def initialize_database():
    conn = sqlite3.connect("study_data.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS server_settings (
        server_id INTEGER PRIMARY KEY,
        channel_id INTEGER
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS study_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        server_id INTEGER NOT NULL,
        channel_id INTEGER NOT NULL,
        start_time DATETIME NOT NULL,
        end_time DATETIME,
        duration_seconds INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()