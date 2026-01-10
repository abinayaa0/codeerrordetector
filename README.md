
# KYC XML Error Classifier

A machine learning project that automatically detects KYC XML request errors using TF-IDF and Logistic Regression.

The system reads SOAP/XML KYC requests, learns patterns that trigger API failures, and predicts likely error codes — without hand-written validation rules.

---

## Features

- Automatically classifies XML into error categories  
- Fast and lightweight (no GPU required)  
- Works offline after training  
- Learns from examples instead of rules  
- Saves trained model to reuse later  
- Easy to retrain when new errors appear  

---

## Project Structure

codeerrordetector/
│
├─ kyc_errors.jsonl            # Training/test dataset
├─ generate_dataset.py         # Script to generate sample XML with errors
├─ loadingdataset.py           # Model training and evaluation
├─ kyc_error_classifier.pkl    # Saved trained model
└─ README.md                   # Documentation

---

## Dataset Format (JSONL)

Each line in `kyc_errors.jsonl` contains:

```json
{
  "request_xml": "<Envelope>...</Envelope>",
  "response_xml": "<Envelope>...</Envelope>",
  "error_label": "VALERR-102"
}
````

`error_label` is the target output.

---

## How the Model Works

### 1. TF-IDF Vectorization

Converts XML text into numeric features by:

* Counting word frequency (TF)
* Boosting rare but meaningful tokens (IDF)
* Down-weighting common XML tags

### 2. Logistic Regression Classifier

Learns correlations such as:

* "invalid" + "pin" → VALERR-102
* "bad user" → AUTHERR-001
* Missing closing tags → XMLERR-001

This approach is simple, fast, reliable, and effective for structured text.

---

## Install Dependencies

Use Python 3.10:

```bash
pip install pandas scikit-learn joblib
```

Note: scikit-learn does not currently support Python 3.13.

---

## Train and Evaluate the Model

Run:

```bash
python loadingdataset.py
```

This script will:

* Load the dataset
* Merge XML text fields
* Split into training and testing sets
* Train the classifier
* Print classification metrics
* Save the model to `kyc_error_classifier.pkl`

---

## Predict Errors from New XML

```python
import joblib

clf = joblib.load("kyc_error_classifier.pkl")

xml_request = "<Envelope> ... </Envelope>"
prediction = clf.predict([xml_request])

print(prediction[0])    # e.g., "VALERR-102"
```

---

## Project Goals

* Learn patterns behind KYC validation failures
* Detect errors without rigid schemas or rule engines
* Complement existing XML validators
* Improve onboarding and debugging efficiency

---

## Future Improvements

* Generate more synthetic samples (500–5000+)
* Balance the number of samples per error type
* Try SVM, Random Forest, or Naive Bayes
* Upgrade to BERT or fine-tune an LLM
* Add rule-based XML checks before ML
* Deploy with FastAPI or Streamlit

---

## Author

Built by Abinaya
Python • Machine Learning • XML processing

---

If you would like enhancements such as:

* requirements.txt
* virtual environment guide
* API deployment instructions
* more datasets
  just ask.

```

---

Done! Drop this directly into your repo 🎉
```
