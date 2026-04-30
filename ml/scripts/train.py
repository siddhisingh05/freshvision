"""
ml/scripts/train.py — Train MobileNetV2 freshness classifier
Run: python train.py
"""
import os
# import numpy as np
# import tensorflow as tf

# ── CONFIG ────────────────────────────────────────────────────
IMG_SIZE       = (224, 224)
BATCH_SIZE     = 32
EPOCHS_FROZEN  = 10   # train only the new head
EPOCHS_FINETUNE = 10  # unfreeze last 20 layers and fine-tune
CLASSES        = ["Spoiled", "Moderately Fresh", "Fresh"]
DATA_DIR       = "../data/processed"
MODEL_SAVE     = "../models/freshness_model.h5"


def build_model():
    """
    MobileNetV2 base + custom freshness classification head.
    TODO: uncomment and implement once TF is installed.
    """
    # base = tf.keras.applications.MobileNetV2(
    #     input_shape=(*IMG_SIZE, 3), include_top=False, weights="imagenet"
    # )
    # base.trainable = False   # freeze for Phase 1
    #
    # x = base.output
    # x = tf.keras.layers.GlobalAveragePooling2D()(x)
    # x = tf.keras.layers.Dense(256, activation="relu")(x)
    # x = tf.keras.layers.Dropout(0.3)(x)
    # output = tf.keras.layers.Dense(len(CLASSES), activation="softmax")(x)
    #
    # model = tf.keras.Model(base.input, output)
    # model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
    # return model
    pass


def train():
    """Load dataset, train in two phases, save model."""
    print("[train] TODO: implement training pipeline")
    # Phase 1 — train head only
    # Phase 2 — unfreeze last 20 layers of MobileNetV2 and fine-tune
    # Save: model.save(MODEL_SAVE)


if __name__ == "__main__":
    train()
