"""
app/utils/inference.py — Load TensorFlow model and run predictions
"""
import numpy as np

LABELS = ["Spoiled", "Moderately Fresh", "Fresh"]
MODEL_PATH = "ml/models/freshness_model.h5"

_model = None   # lazy-loaded singleton


def load_model():
    """Load the TensorFlow model once and cache it."""
    global _model
    if _model is None:
        import tensorflow as tf
        _model = tf.keras.models.load_model(MODEL_PATH)
        print(f"[inference] Model loaded from {MODEL_PATH}")
    return _model


def run_inference(image_array: np.ndarray) -> dict:
    """
    Run model prediction on a preprocessed image array.

    Args:
        image_array: numpy array of shape (1, 224, 224, 3)

    Returns:
        dict with keys: label, confidence, scores
    """
    # TODO: uncomment once model is trained and saved
    # model = load_model()
    # preds = model.predict(image_array)[0]   # shape: (3,)
    # idx = int(np.argmax(preds))
    # return {
    #     "label":      LABELS[idx],
    #     "confidence": float(round(preds[idx], 4)),
    #     "scores": {LABELS[i]: float(round(preds[i], 4)) for i in range(3)},
    # }

    # ── PLACEHOLDER (remove after training) ──────────────────
    return {
        "label": "Fresh",
        "confidence": 0.91,
        "scores": {"Fresh": 0.91, "Moderately Fresh": 0.07, "Spoiled": 0.02},
    }
