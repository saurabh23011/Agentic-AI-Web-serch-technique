# create_db.py

import sqlite3

# Connect to SQLite database (creates example_new.db if it doesn't exist)
connection = sqlite3.connect("example_new.db")
cursor = connection.cursor()

# Create the inventory table
cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    stock_quantity INTEGER NOT NULL
)
""")

# Insert sample data
cursor.executemany("""
INSERT INTO inventory (product_name, stock_quantity) VALUES (?, ?)
""", [
    ("Product A", 150),
    ("Product B", 200),
    ("Product C", 300),
    ("Product D", 100),
    ("Product E", 50)
])

# Commit and close connection
connection.commit()
connection.close()

print("Database created and populated with sample data.")