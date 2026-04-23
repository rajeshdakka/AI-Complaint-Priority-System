# app/services/db_service.py

import sqlite3


def get_db_connection():
    conn = sqlite3.connect(
        "database.db",
        timeout=30,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row
    return conn