import sqlite3
from pathlib import Path

DB_PATH = Path("retail.db")
SCHEMA_PATH = Path("sql/schema.sql")

def main():
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    print("Initialized retail.db")

if __name__ == "__main__":
    main()
