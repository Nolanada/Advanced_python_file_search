import sqlite3

# Initialize SQLite connection
activity_conn = sqlite3.connect('user_activity.db')
activity_cursor = activity_conn.cursor()

# Create a table for user activity
activity_cursor.execute('''
CREATE TABLE IF NOT EXISTS user_activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    activity TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
activity_conn.commit()

# Function to record activity
def record_activity(user_id, activity):
    activity_cursor.execute('INSERT INTO user_activity (user_id, activity) VALUES (?, ?)', (user_id, activity))
    activity_conn.commit()

# Function to get activities of a user
def get_user_activity(user_id):
    activity_cursor.execute('SELECT * FROM user_activity WHERE user_id = ?', (user_id,))
    return activity_cursor.fetchall()
