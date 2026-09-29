def consistency_result(validation, tamper, face):
    reasons = []
    risk_points = 0

    if validation["status"] == "REVIEW":
        risk_points += 1
        reasons.append("Document validation requires review.")

    if tamper["status"] == "ANOMALY REVIEW":
        risk_points += 2
        reasons.append("Image-forensics checks found an anomaly requiring review.")

    if face["status"] == "POSSIBLE MISMATCH":
        risk_points += 2
        reasons.append("Document photo and person photo show low prototype similarity.")
    elif face["status"] == "NOT VERIFIED":
        reasons.append("Face verification could not be completed.")

    if risk_points >= 3:
        risk = "SUSPICIOUS"
    elif risk_points >= 1 or face["status"] == "NOT VERIFIED":
        risk = "REVIEW"
    else:
        risk = "VALID"

    consistency = "Cross-check completed across OCR, validation, visual anomaly checks and face result."
    if not reasons:
        reasons.append("No strong inconsistency was detected by the prototype checks.")

    return {"risk": risk, "reasons": reasons, "consistency": consistency}
