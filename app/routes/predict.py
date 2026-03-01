"""
app/routes/predict.py — Food freshness prediction endpoint
POST /predict — accepts image upload, returns prediction page
"""
import os
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from ..utils.preprocess import preprocess_image
from ..utils.inference import run_inference
from ..models.database import get_db

predict_bp = Blueprint("predict", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@predict_bp.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return render_template("predict.html")

    # --- Handle POST (image upload) ---
    if "file" not in request.files:
        flash("No file uploaded.", "danger")
        return redirect(url_for("predict.predict"))

    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        flash("Please upload a valid image (JPG, PNG, WEBP).", "danger")
        return redirect(url_for("predict.predict"))

    # Save uploaded file
    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    save_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(save_path)

    # Preprocess + run model
    image_array = preprocess_image(save_path)
    result = run_inference(image_array)          # {"label": ..., "confidence": ..., "scores": {...}}

    # Persist to SQLite
    db = get_db()
    db.execute(
        "INSERT INTO predictions (filename, label, confidence) VALUES (?, ?, ?)",
        (filename, result["label"], result["confidence"]),
    )
    db.commit()

    return render_template("result.html", result=result, filename=filename)


@predict_bp.route("/feedback", methods=["POST"])
def feedback():
    prediction_id = request.form.get("prediction_id")
    correct_label = request.form.get("correct_label")
    db = get_db()
    db.execute(
        "INSERT INTO feedback (prediction_id, correct_label) VALUES (?, ?)",
        (prediction_id, correct_label),
    )
    db.commit()
    flash("Thanks for your feedback!", "success")
    return redirect(url_for("history.history"))
