import sqlite3

conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

# 1. Added a missing comma after AUTOINCREMENT
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        done BOOLEAN NOT NULL DEFAULT 0
    )
""")

# 2. Execute the count query
cursor.execute("SELECT COUNT(*) FROM tasks")

# 3. Fetch the first column of the first row (the actual integer count) a tuple
count = cursor.fetchone()[0]
tup = ()
title = ''

# 4. Check if empty and insert initial tasks
if count == 0:
    cursor.execute("INSERT INTO tasks (title) VALUES ('First task')")
    cursor.execute("INSERT INTO tasks (title) VALUES ('Second task')")
    cursor.execute("INSERT INTO tasks (title) VALUES ('Third task')")

    # Commit the changes to permanently save them to the tasks.db file
    conn.commit()

cursor.execute("SELECT title FROM tasks")
rows = cursor.fetchall() # fetch all rows in the DB
for row in rows:
    title = row[0]
    print(title)


conn.close()
