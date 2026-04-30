"""
database.py — SQLite schema and helpers
Author: Yash Upadhyay (ML Lead)
"""
import sqlite3
import os
from flask import g

DATABASE = os.environ.get('DATABASE_URL', 'freshness.db')


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db(app):
    with app.app_context():
        db = get_db()
        db.executescript('''
            CREATE TABLE IF NOT EXISTS users (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                username   TEXT    NOT NULL UNIQUE,
                password   TEXT    NOT NULL,
                security_question TEXT,
                security_answer   TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS predictions (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id        INTEGER NOT NULL REFERENCES users(id),
                filename       TEXT    NOT NULL,
                original_name  TEXT,
                label          TEXT    NOT NULL,
                display_label  TEXT,
                confidence     REAL    NOT NULL,
                probabilities  TEXT,
                created_at     DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS feedback (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                prediction_id INTEGER NOT NULL REFERENCES predictions(id),
                user_id       INTEGER NOT NULL REFERENCES users(id),
                correct_label TEXT    NOT NULL,
                created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        ''')

        existing_columns = {row['name'] for row in db.execute('PRAGMA table_info(users)').fetchall()}
        if 'security_question' not in existing_columns:
            db.execute('ALTER TABLE users ADD COLUMN security_question TEXT')
        if 'security_answer' not in existing_columns:
            db.execute('ALTER TABLE users ADD COLUMN security_answer TEXT')

        db.commit()
