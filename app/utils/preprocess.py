"""
preprocess.py — Image validation and preprocessing for EfficientNetB0
Author: Yash Upadhyay (ML Lead)
"""
import os
import numpy as np
from PIL import Image, UnidentifiedImageError

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp', 'gif'}
ALLOWED_MIMES      = {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}
MAX_FILE_SIZE      = 10 * 1024 * 1024   # 10 MB
IMG_SIZE           = (224, 224)

# ImageNet normalisation constants
IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
IMAGENET_STD  = np.array([0.229, 0.224, 0.225], dtype=np.float32)


def allowed_file(filename: str) -> bool:
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def validate_image(file_path: str) -> tuple[bool, str]:
    """
    Validate an uploaded image file.
    Returns (True, '') on success or (False, error_message) on failure.
    """
    if not os.path.exists(file_path):
        return False, "File not found."

    if os.path.getsize(file_path) > MAX_FILE_SIZE:
        return False, "File exceeds 10 MB limit."

    try:
        with Image.open(file_path) as img:
            fmt = img.format
            if fmt not in ('JPEG', 'PNG', 'WEBP', 'GIF'):
                return False, f"Unsupported image format: {fmt}"
            img.verify()
    except (UnidentifiedImageError, Exception) as e:
        return False, f"Invalid image file: {e}"

    return True, ''


def preprocess_image(image_path: str) -> np.ndarray:
    """
    Load, resize to 224×224, and apply ImageNet normalisation.
    Returns a float32 numpy array of shape (224, 224, 3).
    """
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        img = img.resize(IMG_SIZE, Image.LANCZOS)

    arr = np.array(img, dtype=np.float32) / 255.0
    arr = (arr - IMAGENET_MEAN) / IMAGENET_STD
    return arr
