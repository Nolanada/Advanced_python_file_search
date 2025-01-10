import sqlite3

# Initialize SQLite connection
user_conn = sqlite3.connect('user_management.db')
user_cursor = user_conn.cursor()

# Create a table for user management
user_cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    email TEXT,
    role TEXT
)
''')
user_conn.commit()

# Function to add a new user
def add_user(username, email, role):
    user_cursor.execute('INSERT INTO users (username, email, role) VALUES (?, ?, ?)', (username, email, role))
    user_conn.commit()

# Function to get all users
def get_users():
    user_cursor.execute('SELECT * FROM users')
    return user_cursor.fetchall()

# Function to update user role
def update_user_role(username, role):
    user_cursor.execute('UPDATE users SET role = ? WHERE username = ?', (role, username))
    user_conn.commit()

# Function to delete a user
def delete_user(username):
    user_cursor.execute('DELETE FROM users WHERE username = ?', (username,))
    user_conn.commit()
