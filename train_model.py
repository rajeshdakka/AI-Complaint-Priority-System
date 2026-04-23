# train_model.py

import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# -----------------------------------
# Step 1: Load Dataset from CSV
# -----------------------------------

data = pd.read_csv("dataset.csv")

print("\nDataset Loaded Successfully!\n")
print(data.head())


# -----------------------------------
# Step 2: Input and Output
# -----------------------------------

X = data["issue"]
y = data["priority"]


# -----------------------------------
# Step 3: Train-Test Split
# -----------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# -----------------------------------
# Step 4: Feature Extraction (TF-IDF)
# -----------------------------------

vectorizer = TfidfVectorizer()

X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)


# -----------------------------------
# Step 5: Model Training
# -----------------------------------

model = LogisticRegression()

model.fit(
    X_train_vectorized,
    y_train
)

print("\nModel Training Completed!\n")


# -----------------------------------
# Step 6: Prediction
# -----------------------------------

predictions = model.predict(
    X_test_vectorized
)


# -----------------------------------
# Step 7: Model Evaluation
# -----------------------------------

accuracy = accuracy_score(
    y_test,
    predictions
)

print("Model Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:\n")

print(
    classification_report(
        y_test,
        predictions
    )
)


# -----------------------------------
# Step 8: Save Model + Vectorizer
# -----------------------------------

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("\nModel and Vectorizer saved successfully!")