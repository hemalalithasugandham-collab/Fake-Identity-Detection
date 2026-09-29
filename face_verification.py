import cv2
import numpy as np

def _face_crop(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60,60))
    if len(faces) == 0:
        return None
    x,y,w,h = max(faces, key=lambda r: r[2]*r[3])
    crop = image[y:y+h, x:x+w]
    return crop

def _signature(face):
    gray = cv2.cvtColor(face, cv2.COLOR_RGB2GRAY)
    gray = cv2.resize(gray, (64,64))
    return gray.astype(np.float32) / 255.0

def verify_face(document_image, person_image):
    a = _face_crop(document_image)
    b = _face_crop(person_image)

    if a is None or b is None:
        return {
            "status": "NOT VERIFIED",
            "score": 0.0,
            "message": "Face not detected in one or both images."
        }

    sa, sb = _signature(a), _signature(b)
    # Prototype similarity only; not a biometric identity decision.
    score = float(1.0 - np.mean(np.abs(sa - sb)))
    status = "MATCH" if score >= 0.72 else "POSSIBLE MISMATCH"

    return {
        "status": status,
        "score": score,
        "message": f"Prototype face similarity: {score:.2f}"
    }
