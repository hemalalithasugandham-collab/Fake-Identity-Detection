import cv2
import numpy as np

def detect_tamper(image):
    # Demo-level image-forensics heuristic: edge/noise inconsistency + compression-error style analysis.
    bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 80, 160)
    edge_density = float(np.mean(edges > 0))

    # ELA-like recompression difference.
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    ok, enc = cv2.imencode(".jpg", bgr, encode_param)
    if ok:
        recompressed = cv2.imdecode(enc, cv2.IMREAD_COLOR)
        diff = cv2.absdiff(bgr, recompressed)
        ela_score = float(np.mean(diff)) / 255.0
    else:
        ela_score = 0.0

    score = min(1.0, (ela_score * 2.5) + (edge_density * 0.8))
    status = "ANOMALY REVIEW" if score >= 0.35 else "NO STRONG ANOMALY"

    return {
        "score": score,
        "status": status,
        "edge_density": edge_density,
        "ela_score": ela_score
    }
