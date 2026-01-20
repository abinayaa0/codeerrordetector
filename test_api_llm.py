import requests
import json

url = "http://127.0.0.1:8000/auto-fix-xml"
payload = {
    "xml": "<KYC><PIN>123</PIN>",
    "error_code": "XMLERR-001",
    "confidence": 0.98
}

print(f"Sending request to {url}...")
try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
