from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# Sample training data
X = [
    "Flood in village urgent help needed",
    "Road damaged after heavy rain",
    "Electricity issue in street",
    "Tree fallen on road",
    "Water leakage in home",
    "Bridge collapsed urgent rescue needed",
    "Garbage issue in colony",
    "Fire accident immediate response needed",
    "Hospital emergency ambulance required",
    "Street light not working"
]

y = [
    "High",
    "Medium",
    "Low",
    "Medium",
    "Low",
    "High",
    "Low",
    "High",
    "High",
    "Low"
]

# Vectorizer
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Model
model = LogisticRegression()
model.fit(X_vectorized, y)

# Save vectorizer
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model and Vectorizer saved successfully!")