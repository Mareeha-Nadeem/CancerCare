import sqlite3
import sys

# Force output to stderr to avoid buffering
def log(msg):
    print(msg, file=sys.stderr, flush=True)

log("Checking database...")

conn = sqlite3.connect('cancercare.db')
cursor = conn.cursor()

# Check if post_diagnosis table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='post_diagnosis';")
result = cursor.fetchone()

if result:
    log("post_diagnosis table EXISTS")
    
    # Get the columns
    cursor.execute('PRAGMA table_info(post_diagnosis);')
    columns = cursor.fetchall()
    
    log(f"\nColumns in post_diagnosis table:")
    for col in columns:
        log(f"  - {col[1]} ({col[2]})")
    
    # Check for grade
    has_grade = any(col[1] == 'grade' for col in columns)
    log(f"\nHas 'grade' column: {has_grade}")
else:
    log("post_diagnosis table DOES NOT EXIST!")

conn.close()
log("\nDone!")
