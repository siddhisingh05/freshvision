"""
ml/scripts/evaluate.py — Generate accuracy, F1, confusion matrix
Run: python evaluate.py
"""
CLASSES = ["Spoiled", "Moderately Fresh", "Fresh"]
MODEL_PATH = "../models/freshness_model.h5"
TEST_DIR   = "../data/processed/test"


def evaluate():
    """
    Load saved model, run on test set, print metrics, save confusion matrix plot.
    TODO: implement once model is trained.
    """
    # import tensorflow as tf
    # from sklearn.metrics import classification_report, confusion_matrix
    # import seaborn as sns, matplotlib.pyplot as plt
    #
    # model = tf.keras.models.load_model(MODEL_PATH)
    # test_ds = tf.keras.preprocessing.image_dataset_from_directory(
    #     TEST_DIR, image_size=(224, 224), batch_size=32, label_mode="categorical"
    # )
    # y_true, y_pred = [], []
    # for images, labels in test_ds:
    #     preds = model.predict(images)
    #     y_pred.extend(preds.argmax(axis=1))
    #     y_true.extend(labels.numpy().argmax(axis=1))
    #
    # print(classification_report(y_true, y_pred, target_names=CLASSES))
    #
    # cm = confusion_matrix(y_true, y_pred)
    # sns.heatmap(cm, annot=True, fmt="d", xticklabels=CLASSES, yticklabels=CLASSES)
    # plt.savefig("../models/confusion_matrix.png")
    print("[evaluate] TODO: implement after training")


if __name__ == "__main__":
    evaluate()
