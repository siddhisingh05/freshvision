"""
predict.py — Image upload and freshness classification route
Author: Siddhi Singh (Full-Stack Lead)
"""
import os
import uuid
import json
from functools import wraps
from flask import (Blueprint, render_template, request,
                   redirect, url_for, session, flash, current_app)
from werkzeug.utils import secure_filename
from app.models.database import get_db
from app.utils.preprocess import allowed_file, validate_image
from app.utils.inference import run_inference

predict_bp = Blueprint('predict', __name__)

UPLOAD_FOLDER  = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please sign in to continue.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@predict_bp.route('/predict', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'GET':
        return render_template('predict.html')

    # ── File validation ───────────────────────────────────────
    if 'image' not in request.files:
        flash('No file selected.', 'danger')
        return render_template('predict.html')

    file = request.files['image']

    if file.filename == '':
        flash('No file selected.', 'danger')
        return render_template('predict.html')

    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload JPG, PNG, or WEBP.', 'danger')
        return render_template('predict.html')

    # ── Save with UUID filename ───────────────────────────────
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    original_name = secure_filename(file.filename)
    ext           = original_name.rsplit('.', 1)[1].lower()
    safe_filename = f"{uuid.uuid4().hex}.{ext}"
    save_path     = os.path.join(UPLOAD_FOLDER, safe_filename)
    file.save(save_path)

    # ── Validate image content ────────────────────────────────
    ok, err = validate_image(save_path)
    if not ok:
        os.remove(save_path)
        flash(f'Invalid image: {err}', 'danger')
        return render_template('predict.html')

    # ── Run inference ─────────────────────────────────────────
    result = run_inference(save_path)

    # ── Persist to DB ─────────────────────────────────────────
    db = get_db()
    cur = db.execute(
        '''INSERT INTO predictions
           (user_id, filename, original_name, label, display_label, confidence, probabilities)
           VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (
            session['user_id'],
            safe_filename,
            original_name,
            result['label'],
            result['display_label'],
            result['confidence'],
            json.dumps(result.get('probabilities', {})),
        )
    )
    db.commit()
    prediction_id = cur.lastrowid

    return render_template(
        'result.html',
        filename      = safe_filename,
        original_name = original_name,
        label         = result['label'],
        display_label = result['display_label'],
        confidence    = result['confidence'],
        probabilities = result.get('probabilities', {}),
        prediction_id = prediction_id,
    )
