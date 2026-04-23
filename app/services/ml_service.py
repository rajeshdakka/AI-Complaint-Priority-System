import pickle
import os

# Base project path
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "vectorizer.pkl")

# Load trained files
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

with open(VECTORIZER_PATH, "rb") as f:
    vectorizer = pickle.load(f)


def predict_priority(issue):
    """
    Predict complaint priority using ML model
    """

    text_vector = vectorizer.transform([issue])

    prediction = model.predict(text_vector)[0]

    probabilities = model.predict_proba(text_vector)

    confidence = float(max(probabilities[0]))

    return prediction, confidence