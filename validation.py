import re
from datetime import datetime

def validate_document(text):
    t = text.lower()
    checks = []
    if len(text.strip()) < 10:
        checks.append("Very little readable text detected")
    else:
        checks.append("Readable text detected")

    date_matches = re.findall(r"\b(20\d{2})[-/](\d{1,2})[-/](\d{1,2})\b", text)
    expired = False
    for y, m, d in date_matches:
        try:
            dt = datetime(int(y), int(m), int(d))
            if dt < datetime.now():
                expired = True
        except ValueError:
            pass

    if expired:
        checks.append("A detected date may be expired")

    status = "REVIEW" if any("expired" in x.lower() for x in checks) else "PASS"
    return {"status": status, "checks": checks}
