#!/bin/bash

# Initialize the database
python -c "
import sqlite3
conn = sqlite3.connect('config.db')
cursor = conn.cursor()

# Create settings table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    )
''')

# Create filters table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS filters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT UNIQUE
    )
''')

# Create conversation_map table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS conversation_map (
        thread_id TEXT PRIMARY KEY,
        whatsapp_user_number TEXT,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()
print('Database initialized successfully')
"

# Start the background worker in the background
echo "Starting background worker..."
python worker.py &

# Start the Flask web application with gunicorn
echo "Starting web server..."
exec gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 app:app 