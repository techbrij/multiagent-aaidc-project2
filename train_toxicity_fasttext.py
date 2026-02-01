"""
train_toxicity_fasttext.py

This script trains a fastText model for toxicity detection using a labeled dataset.
The dataset should be in fastText supervised format:
    __label__toxic This is a toxic sentence.
    __label__not_toxic This is a non-toxic sentence.

You can use any public dataset (e.g., Jigsaw Toxic Comment Classification) and preprocess it to this format.
"""
import fasttext
import os

# Path to your training data (update this as needed)
TRAIN_DATA_PATH = "data/toxicity_train.txt"
MODEL_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "src", "tools", "toxicity_model.bin")

# Training parameters (adjust as needed)
EPOCHS = 10
LR = 0.1
WORD_NGRAMS = 2
DIM = 100

if __name__ == "__main__":
    if not os.path.exists(TRAIN_DATA_PATH):
        raise FileNotFoundError(f"Training data not found at {TRAIN_DATA_PATH}. Please provide a labeled dataset.")
    print(f"Training fastText model on {TRAIN_DATA_PATH}...")
    model = fasttext.train_supervised(
        input=TRAIN_DATA_PATH,
        epoch=EPOCHS,
        lr=LR,
        wordNgrams=WORD_NGRAMS,
        dim=DIM,
        verbose=2
    )
    model.save_model(MODEL_OUTPUT_PATH)
    print(f"Model saved to {MODEL_OUTPUT_PATH}")
