"""
app/models/database.py — SQLite database setup using Flask's built-in sqlite3
"""
import sqlite3
import click
from flask import current_app, g


def get_db():
    """Open a new database connection for the current request."""
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    """Create tables and register teardown on the Flask app."""
    with app.app_context():
        db = sqlite3.connect(app.config["DATABASE"])
        db.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                filename  TEXT NOT NULL,
                label     TEXT NOT NULL,
                confidence REAL NOT NULL,
                category  TEXT DEFAULT 'unknown',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                prediction_id INTEGER REFERENCES predictions(id),
                correct_label TEXT NOT NULL,
                created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.commit()
        db.close()
    app.teardown_appcontext(close_db)
