"""
inference.py — Calls HuggingFace Gradio Space API for freshness prediction.
Falls back to local .h5 model if HF is unavailable.
Author: Yash Upadhyay (ML Lead)
"""
import os
import base64
import json
import requests
from pathlib import Path

HF_SPACE_URL = os.environ.get(
    'HF_SPACE_URL',
    'https://lazypanda0103-unified-comprehensive-freshness-clas.hf.space'
)

LABEL_MAP = {
    'fresh':     {'display': 'Fresh',      'key': 'fresh'},
    'semifresh': {'display': 'Semi-Fresh', 'key': 'semi'},
    'semi':      {'display': 'Semi-Fresh', 'key': 'semi'},
    'semi-fresh':{'display': 'Semi-Fresh', 'key': 'semi'},
    'rotten':    {'display': 'Rotten',     'key': 'stale'},
    'stale':     {'display': 'Rotten',     'key': 'stale'},
    'spoiled':   {'display': 'Rotten',     'key': 'stale'},
}


def _normalise(raw_label: str) -> dict:
    key = raw_label.lower().replace(' ', '').replace('-', '')
    mapped = LABEL_MAP.get(key, LABEL_MAP.get(raw_label.lower(), None))
    if mapped:
        return mapped
    return {'display': raw_label.title(), 'key': 'stale'}


def run_inference(image_path: str) -> dict:
    """
    Run freshness inference on an image file.
    Returns:
        {
            label: str          — normalised key (fresh/semi/stale)
            display_label: str  — human label (Fresh/Semi-Fresh/Rotten)
            confidence: float   — 0-100
            probabilities: dict — {class_name: probability}
        }
    """
    # ── Try HuggingFace Gradio API first ─────────────────────
    try:
        with open(image_path, 'rb') as f:
            img_b64 = base64.b64encode(f.read()).decode()

        ext = Path(image_path).suffix.lstrip('.').lower()
        mime = 'image/jpeg' if ext in ('jpg', 'jpeg') else f'image/{ext}'

        payload = {
            "data": [{"data": f"data:{mime};base64,{img_b64}", "name": Path(image_path).name}]
        }

        resp = requests.post(
            f"{HF_SPACE_URL}/run/predict",
            json=payload,
            timeout=20
        )
        resp.raise_for_status()
        result = resp.json()

        # Parse Gradio response
        data = result.get('data', [{}])[0]
        if isinstance(data, dict):
            raw_label   = data.get('label', 'unknown')
            confidences = data.get('confidences', [])
        else:
            raw_label   = str(data)
            confidences = []

        normalised = _normalise(raw_label)

        # Build probabilities dict
        probs = {}
        top_conf = 0.0
        for c in confidences:
            lbl = c.get('label', '')
            val = float(c.get('confidence', 0))
            norm = _normalise(lbl)
            probs[norm['display']] = val
            if lbl.lower().replace(' ', '') == raw_label.lower().replace(' ', ''):
                top_conf = val * 100

        if not top_conf and confidences:
            top_conf = float(confidences[0].get('confidence', 0)) * 100

        return {
            'label':         normalised['key'],
            'display_label': normalised['display'],
            'confidence':    round(top_conf, 1),
            'probabilities': probs,
        }

    except Exception as hf_err:
        print(f"[inference] HF API failed: {hf_err} — trying local fallback")

    # ── Local .h5 fallback ────────────────────────────────────
    try:
        import numpy as np
        import tensorflow as tf
        from app.utils.preprocess import preprocess_image

        model_path = os.path.join(os.path.dirname(__file__), '..', '..', 'ml', 'models', 'freshness_model.h5')
        model_path = os.path.abspath(model_path)

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Local model not found at {model_path}")

        model = tf.keras.models.load_model(model_path)
        img_array = preprocess_image(image_path)
        preds = model.predict(np.expand_dims(img_array, axis=0))[0]

        classes = ['Fresh', 'Semi-Fresh', 'Rotten']
        idx = int(np.argmax(preds))
        raw = classes[idx]
        normalised = _normalise(raw)
        probs = {c: float(preds[i]) for i, c in enumerate(classes)}

        return {
            'label':         normalised['key'],
            'display_label': normalised['display'],
            'confidence':    round(float(preds[idx]) * 100, 1),
            'probabilities': probs,
        }

    except Exception as local_err:
        print(f"[inference] Local fallback also failed: {local_err}")

    # ── Total failure fallback ────────────────────────────────
    return {
        'label':         'stale',
        'display_label': 'Unknown',
        'confidence':    0.0,
        'probabilities': {},
    }
