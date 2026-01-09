clf = joblib.load("kyc_error_classifier.pkl")
xml = "<Envelope>...</Envelope>"
prediction = clf.predict([xml])
print(prediction[0])
