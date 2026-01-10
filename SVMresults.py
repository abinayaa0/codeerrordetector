import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
import joblib

# Load JSONL dataset
df = pd.read_json("kyc_errors.jsonl", lines=True)

# Combine request + response into a single input string
df["input"] = df["request_xml"] + " " + df["response_xml"]

# Train-test split (stratified so all classes appear)
train, test = train_test_split(
    df,
    test_size=0.2,
    stratify=df["error_label"]
)

# SVM Pipeline (TF-IDF + LinearSVC)
model = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=50000)),
    ("clf", LinearSVC())
])

# Train
model.fit(train["input"], train["error_label"])

# Predict on test set
preds = model.predict(test["input"])

# Show results
print(classification_report(test["error_label"], preds))

# Save model
joblib.dump(model, "kyc_error_classifier_svm.pkl")
print("SVM model saved successfully")
