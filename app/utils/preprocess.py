"""
app/utils/preprocess.py — Image preprocessing for model inference
"""
import numpy as np
from PIL import Image

IMG_SIZE = (224, 224)


def preprocess_image(image_path: str) -> np.ndarray:
    """
    Load an image from disk, resize to 224x224, normalize to [0, 1].
    Returns a numpy array of shape (1, 224, 224, 3) ready for model input.
    """
    img = Image.open(image_path).convert("RGB")
    img = img.resize(IMG_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0
    return np.expand_dims(arr, axis=0)   # shape: (1, 224, 224, 3)
