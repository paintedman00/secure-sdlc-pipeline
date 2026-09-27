import sqlite3

from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL
);
"""

SEED_USERS = [
    ("alice", "alice@example.com"),
    ("bob", "bob@example.com"),
    ("carol", "carol@example.com"),
]


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(exc=None):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


def init_db():
    conn = get_db()
    conn.executescript(SCHEMA)
    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO users (username, email) VALUES (?, ?)", SEED_USERS
        )
        conn.commit()


def init_app(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()
