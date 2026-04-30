"""
predict.py — Image upload and freshness classification route
Author: Siddhi Singh (Full-Stack Lead)
"""
import io
import json
import os
import uuid
from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from PIL import Image
from werkzeug.utils import secure_filename

from app.ml_model.inference import predict_image
from app.models.database import get_db
from app.utils.preprocess import allowed_file

predict_bp = Blueprint('predict', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')


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

    if 'file' not in request.files:
        flash('No file selected.', 'danger')
        return render_template('predict.html')

    file = request.files['file']
    if file.filename == '':
        flash('No file selected.', 'danger')
        return render_template('predict.html')

    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload JPG, PNG, or WEBP.', 'danger')
        return render_template('predict.html')

    original_name = secure_filename(file.filename)
    ext = original_name.rsplit('.', 1)[1].lower()
    safe_filename = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(UPLOAD_FOLDER, safe_filename)

    file_bytes = file.read()
    try:
        with Image.open(io.BytesIO(file_bytes)) as pil_image:
            pil_image = pil_image.convert('RGB')
            ml_result = predict_image(pil_image)
    except Exception as exc:
        flash(f'Error processing image: {exc}', 'danger')
        return render_template('predict.html')

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    with open(save_path, 'wb') as output_file:
        output_file.write(file_bytes)

    result = {
        'fruit': ml_result['fruit'],
        'condition': ml_result['condition'],
        'confidence': ml_result['confidence'],
        'label': 'fresh' if ml_result['condition'] == 'Fresh' else 'stale',
        'display_label': ml_result['condition'],
    }

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
            json.dumps({}),
        )
    )
    db.commit()
    prediction_id = cur.lastrowid

    return render_template(
        'result.html',
        filename=safe_filename,
        original_name=original_name,
        fruit=result['fruit'],
        condition=result['condition'],
        confidence=result['confidence'],
        label=result['label'],
        display_label=result['display_label'],
        prediction_id=prediction_id,
    )
