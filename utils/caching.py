import sqlite3
from cachetools import cached, TTLCache

# Initialize in-memory cache
#memory_cache = TTLCache(maxsize=100, ttl=300)
def drop_cache_table(): 
    conn = sqlite3.connect('cache.db') 
    cursor = conn.cursor() 
    cursor.execute('DROP TABLE IF EXISTS cache') 
    conn.commit() 
    conn.close() 
drop_cache_table()
# SQLite connection
conn = sqlite3.connect('cache.db')
cursor = conn.cursor()

# Create a table for caching
cursor.execute('''
 CREATE TABLE IF NOT EXISTS cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT UNIQUE,
            results TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
''')
conn.commit()

def cache_results(query, results):
    conn = sqlite3.connect('cache.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO cache (query, results)
        VALUES (?, ?)
    ''', (query, results))
    conn.commit()
    conn.close()

def get_cached_results(query):
    conn = sqlite3.connect('cache.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT results FROM cache WHERE query = ?
    ''', (query,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

