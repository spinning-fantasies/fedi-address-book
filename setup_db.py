import json
import sqlite3

# Read JSON data
with open('followers.json', 'r') as json_file:
    followers_data = json.load(json_file)

# Setup SQLite database
conn = sqlite3.connect('followers.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS followers (
        id INTEGER PRIMARY KEY,
        created_at TEXT,
        display_name TEXT,
        acct TEXT,
        location TEXT,
        is_deleted INTEGER DEFAULT 0
    );
''')

# Insert data into SQLite
for follower in followers_data:
    cursor.execute('''
        INSERT INTO followers (created_at, display_name, acct)
        VALUES (?, ?, ?)
    ''', (follower['created_at'], follower['display_name'], follower['acct']))

conn.commit()
conn.close()
