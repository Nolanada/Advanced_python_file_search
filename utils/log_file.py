# utils/logging.py
import sqlite3

# Initialize SQLite connection
log_conn = sqlite3.connect('logs.db')
log_cursor = log_conn.cursor()

# Create tables
log_cursor.execute('''
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    log_level TEXT,
    message TEXT
)
''')
log_conn.commit()

def log_event(log_level, message):
    log_cursor.execute('INSERT INTO logs (log_level, message) VALUES (?, ?)', (log_level, message))
    log_conn.commit()

def get_logs(log_level):
    log_cursor.execute('SELECT * FROM logs WHERE log_level = ?', (log_level,))
    return log_cursor.fetchall()
