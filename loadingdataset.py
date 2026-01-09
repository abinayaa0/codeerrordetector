import pandas as pd
from sklearn.model_selection import train_test_split
import joblib

#loading the dataset
df = pd.read_json("kyc_errors.jsonl", lines=True)
df["input"] = df["request_xml"] + " " + df["response_xml"]

#train_test_split dataset

train, test = train_test_split(
    df,
    test_size=0.2,
    stratify=df["error_label"]
)

#creating adn training the model
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

model = Pipeline([
    ("tfidf", TfidfVectorizer(max_features=50000)),
    ("clf", LogisticRegression(max_iter=1000))
])

model.fit(train["input"], train["error_label"])

#Evaluation
from sklearn.metrics import classification_report

preds = model.predict(test["input"])
print(classification_report(test["error_label"], preds))


#Saving the model:

joblib.dump(model, "kyc_error_classifier.pkl")
print("model successfully saved")



