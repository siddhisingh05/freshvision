"""
ml/scripts/preprocess.py — Dataset download, clean, augment, split
Run: python preprocess.py
"""
RAW_DIR       = "../data/raw"
PROCESSED_DIR = "../data/processed"
SPLIT         = (0.70, 0.15, 0.15)   # train / val / test

def run():
    """Resize images, apply augmentation config, save train/val/test splits."""
    # TODO: implement using tf.keras.preprocessing or torchvision
    print("[preprocess] TODO: implement dataset pipeline")

if __name__ == "__main__":
    run()
