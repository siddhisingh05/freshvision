"""
test_inference.py — Unit tests for ML pipeline
Author: Yash Upadhyay (ML Lead)
Run: pytest tests/ -v
"""
import os
import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from PIL import Image
import tempfile

# ── Preprocess tests ──────────────────────────────────────────

def make_temp_image(color=(180, 220, 130), fmt='JPEG'):
    tmp = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
    img = Image.new('RGB', (256, 256), color=color)
    img.save(tmp.name, format=fmt)
    return tmp.name


def test_preprocess_output_shape():
    from app.utils.preprocess import preprocess_image
    path = make_temp_image()
    try:
        arr = preprocess_image(path)
        assert arr.shape == (224, 224, 3), f"Expected (224,224,3), got {arr.shape}"
    finally:
        os.unlink(path)


def test_preprocess_dtype():
    from app.utils.preprocess import preprocess_image
    path = make_temp_image()
    try:
        arr = preprocess_image(path)
        assert arr.dtype == np.float32
    finally:
        os.unlink(path)


def test_preprocess_normalised_range():
    """ImageNet normalisation should produce values roughly in [-3, 3]."""
    from app.utils.preprocess import preprocess_image
    path = make_temp_image()
    try:
        arr = preprocess_image(path)
        assert arr.min() > -4.0
        assert arr.max() <  4.0
    finally:
        os.unlink(path)


def test_validate_image_valid():
    from app.utils.preprocess import validate_image
    path = make_temp_image()
    try:
        ok, msg = validate_image(path)
        assert ok, f"Expected valid image, got: {msg}"
    finally:
        os.unlink(path)


def test_validate_image_missing():
    from app.utils.preprocess import validate_image
    ok, msg = validate_image('/nonexistent/path/image.jpg')
    assert not ok
    assert 'not found' in msg.lower()


def test_allowed_file_valid():
    from app.utils.preprocess import allowed_file
    for name in ['photo.jpg', 'food.jpeg', 'test.png', 'img.webp']:
        assert allowed_file(name), f"{name} should be allowed"


def test_allowed_file_invalid():
    from app.utils.preprocess import allowed_file
    for name in ['script.exe', 'data.csv', 'file.pdf', 'noextension']:
        assert not allowed_file(name), f"{name} should not be allowed"


# ── Inference output structure tests ─────────────────────────

@patch('requests.post')
def test_inference_returns_required_keys(mock_post):
    """inference result must always contain label, display_label, confidence, probabilities."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = {
        'data': [{'label': 'fresh', 'confidences': [
            {'label': 'fresh', 'confidence': 0.92},
            {'label': 'semi-fresh', 'confidence': 0.05},
            {'label': 'rotten', 'confidence': 0.03},
        ]}]
    }
    mock_resp.raise_for_status = MagicMock()
    mock_post.return_value = mock_resp

    from app.utils.inference import run_inference
    path = make_temp_image()
    try:
        result = run_inference(path)
        for key in ('label', 'display_label', 'confidence', 'probabilities'):
            assert key in result, f"Missing key: {key}"
        assert result['label'] in ('fresh', 'semi', 'stale')
        assert 0 <= result['confidence'] <= 100
    finally:
        os.unlink(path)


@patch('requests.post', side_effect=Exception("Network error"))
def test_inference_fallback_on_hf_failure(mock_post):
    """When HF API fails and no local model exists, should return safe defaults."""
    from app.utils.inference import run_inference
    path = make_temp_image()
    try:
        result = run_inference(path)
        assert 'label' in result
        assert 'confidence' in result
    finally:
        os.unlink(path)
