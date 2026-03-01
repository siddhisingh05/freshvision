"""
app/routes/history.py — Prediction history page
GET /history — shows all past predictions from SQLite
"""
from flask import Blueprint, render_template
from ..models.database import get_db

history_bp = Blueprint("history", __name__)


@history_bp.route("/history")
def history():
    db = get_db()
    predictions = db.execute(
        "SELECT * FROM predictions ORDER BY created_at DESC LIMIT 50"
    ).fetchall()
    return render_template("history.html", predictions=predictions)
