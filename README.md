# Code Error Detector & Auto-Fixer

A comprehensive system for detecting, localizing, and automatically fixing errors in KYC XML requests. This project combines Machine Learning for classification with a dual-strategy (Rule-based + LLM) engine for remediation.

---

## Features

### 1. ML Error Classification
- **Technology**: TF-IDF Vectorization + Logistic Regression / SVM.
- **Function**: Predicts error codes (e.g., `VALERR-102`) from raw XML patterns.
- **Performance**: High accuracy on known error types.
- **Offline**: Works without external dependencies after training.

### 2. Auto-Remediation Engine
- **Localization**: Pinpoints exactly where the error occurred in the XML (Tag, Value, or Structure).
- **Hybrid Fix Strategy**:
    - **Rule-Based**: Deterministic fixes for known formats (e.g., padding PINs, formatting dates).
    - **LLM-Based**: Uses `Qwen2.5-Coder` (via Ollama) to repair complex structural XML errors (missing tags, malformed syntax).
- **Reliability**: Includes retry logic (max 2 retries) and validation for LLM outputs.

### 3. API Service
- **FastAPI**: Provides a REST endpoint to classify and fix errors in real-time.
- **Swagger UI**: Interactive documentation at `/docs`.

---

## Project Structure

```text
codeerrordetector/
│
├── api.py                  # FastAPI application entry point
├── kyc_errors.jsonl        # Training dataset
├── README.md               # This file
│
├── engine/                 # Core Logic
│   ├── localize.py         # Error localization (Field/XML Structure)
│   ├── fix_rules.py        # Deterministic fixes (PIN, Date)
│   ├── llm_fix.py          # LLM integration (Ollama/Qwen)
│   ├── orchestrator.py     # Manages the fix workflow
│   └── error_registry.py   # Definitions of errors and strategies
│
├── utils/
│   └── xml_utils.py        # XML parsing helpers
│
└── [Scripts]
    ├── generate_dataset.py # Create synthetic training data
    ├── loadingdataset.py   # Train and save ML models
    └── test_*.py           # Verification scripts
```

---

## Installation

### Prerequisites
1.  **Python 3.13** (Recommended for API/Engine)
2.  **Ollama** (Required for LLM fixes)
    - Install Ollama from [ollama.com](https://ollama.com)
    - Pull the model: `ollama pull qwen2.5-coder`

### Dependencies
```bash
pip install fastapi uvicorn requests
# For ML training (requires Python 3.10 due to scikit-learn limits):
pip install pandas scikit-learn joblib
```

---

## Usage

### 1. Start the API Server
Run the FastAPI server using `uvicorn`:
```powershell
& C:/Path/To/Python313/python.exe -m uvicorn api:app --reload
```
*Server runs on `http://127.0.0.1:8000`*

### 2. Auto-Fix an Error (Example)
Send a POST request to `/auto-fix-xml`:

```bash
curl -X POST "http://127.0.0.1:8000/auto-fix-xml" \
     -H "Content-Type: application/json" \
     -d '{
           "xml": "<KYC><PIN>123</PIN></KYC>",
           "error_code": "VALERR-102",
           "confidence": 0.98
         }'
```

**Response:**
```json
{
  "error_code": "VALERR-102",
  "fix_strategy": "rule",
  "auto_fix_applied": true,
  "original_value": "123",
  "fixed_value": "000123",
  "explanation": "Invalid PIN code format"
}
```

### 3. Train the ML Model
(Use Python 3.10)
```bash
python loadingdataset.py
```
This processes `kyc_errors.jsonl` and saves `kyc_error_classifier.pkl`.

---

## Testing

We have included several test scripts to verify different components:

| Script | Purpose |
| :--- | :--- |
| `test_localize.py` | Checks if the system correctly identifies the location of errors. |
| `test_fix_engine.py` | Verifies the orchestrator logic for Rule-based fixes. |
| `test_llm_fix.py` | Tests the Ollama integration for fixing structural XML errors. |
| `test_valerr_103.py` | Verifies the specific Date Format fix. |
| `test_api_llm.py` | End-to-end test of the API calling the LLM. |

Run any test:
```powershell
python test_llm_fix.py
```

---

## System Logic

### Fix Selection Strategy
The `process_xml` function decides how to handle an error based on `engine/fix_selector.py`:

1.  **Check Registry**: Is the error known? (`error_registry.py`)
2.  **Check Fixability**: Is `fixable=True`?
3.  **Check Confidence**: Is the detection confidence > 0.90?
4.  **Select Strategy**:
    - `rule`: Use `fix_rules.py` (Fast, 100% reliable).
    - `llm`: Use `llm_fix.py` (For complex structure, creates new valid XML).
    - `none`: Return diagnosis only.

### LLM Robustness
The LLM integration uses a **Retry Mechanism** (Max 2 retries) and a prompt engineered for XML structure repair. It validates output via `xml_validator.py` before accepting it.
