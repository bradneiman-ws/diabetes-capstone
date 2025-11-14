# src/db_utils.py
from pathlib import Path
import sqlite3
from project_paths import PROJECT_ROOT

def connect_to_db(db_name: str = "diabetes.db") -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Connect to an SQLite database located in the /data folder.

    Args:
        db_name: Filename of the SQLite database (default: 'diabetes.db').

    Returns:
        (conn, cursor) tuple ready for queries.
    """
    db_path = PROJECT_ROOT / "data" / db_name
    if not db_path.exists():
        raise FileNotFoundError(f"❌ Database not found: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print(f"✅ Connected to database: {db_path}")
    return conn, cursor

def close_db(conn):
    """Close the SQLite connection."""
    if conn:
        conn.close()
        print("🔒 Connection closed.")