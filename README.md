# TRACE-ID Prototype

A hackathon prototype for AI-based fake identity and document screening.

## Pipeline
Upload → OCR → Validation → Tamper/Anomaly Check → Face Check → Consistency Mapping → Risk + Evidence

## Run locally

```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Then:
```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the local Streamlit URL shown in the terminal.

## Important
This is a prototype decision-support system. The tamper and face components use lightweight demo heuristics and must not be treated as authoritative identity or forensic verification.
Use only synthetic/sample documents for testing.
