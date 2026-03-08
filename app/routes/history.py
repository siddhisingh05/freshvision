"""
history.py — Prediction history with pagination and feedback submission
Author: Siddhi Singh (Full-Stack Lead)
"""
import json
from functools import wraps
from flask import (Blueprint, render_template, request,
                   redirect, url_for, session, flash)
from app.models.database import get_db

history_bp = Blueprint('history', __name__)
PER_PAGE = 20


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please sign in to continue.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@history_bp.route('/history')
@login_required
def view_history():
    db           = get_db()
    label_filter = request.args.get('label', '').strip().lower()
    page         = max(1, int(request.args.get('page', 1)))
    offset       = (page - 1) * PER_PAGE
    user_id      = session['user_id']

    # Base query
    base_where = 'WHERE user_id = ?'
    params     = [user_id]

    if label_filter:
        base_where += ' AND label = ?'
        params.append(label_filter)

    total = db.execute(
        f'SELECT COUNT(*) FROM predictions {base_where}', params
    ).fetchone()[0]

    rows = db.execute(
        f'''SELECT id, filename, original_name, label, display_label,
                   confidence, created_at
            FROM predictions {base_where}
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?''',
        params + [PER_PAGE, offset]
    ).fetchall()

    total_pages = max(1, (total + PER_PAGE - 1) // PER_PAGE)

    return render_template(
        'history.html',
        rows         = rows,
        page         = page,
        total_pages  = total_pages,
        label_filter = label_filter,
        total        = total,
    )


@history_bp.route('/feedback', methods=['POST'])
@login_required
def submit_feedback():
    prediction_id = request.form.get('prediction_id')
    correct_label = request.form.get('correct_label', '').strip()

    allowed_labels = {'Fresh', 'Semi-Fresh', 'Rotten'}
    if not prediction_id or correct_label not in allowed_labels:
        flash('Invalid feedback submission.', 'danger')
        return redirect(url_for('history.view_history'))

    db = get_db()
    # Verify prediction belongs to this user
    pred = db.execute(
        'SELECT id FROM predictions WHERE id = ? AND user_id = ?',
        (prediction_id, session['user_id'])
    ).fetchone()

    if not pred:
        flash('Prediction not found.', 'danger')
        return redirect(url_for('history.view_history'))

    db.execute(
        'INSERT INTO feedback (prediction_id, user_id, correct_label) VALUES (?, ?, ?)',
        (prediction_id, session['user_id'], correct_label)
    )
    db.commit()
    flash('Thank you for your feedback!', 'success')
    return redirect(url_for('history.view_history'))
