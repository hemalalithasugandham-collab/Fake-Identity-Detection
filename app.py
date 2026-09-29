import streamlit as st
from PIL import Image
import numpy as np
import re
from datetime import datetime

from modules.ocr import extract_text
from modules.validation import validate_document
from modules.tamper_detection import detect_tamper
from modules.face_verification import verify_face
from modules.consistency import consistency_result


st.set_page_config(
    page_title="TRACE-ID",
    page_icon="🔎",
    layout="wide"
)

st.title("TRACE-ID")
st.caption("AI-Based Fake Identity & Document Screening — Prototype")


# Expiry date check
def check_expiry(ocr_text):

    patterns = [
        r"EXP\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})",
        r"EXP\s*[:\-]?\s*(\d{2}-\d{2}-\d{4})",
        r"EXPIRATION\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})"
    ]

    expiry_date = None

    for pattern in patterns:
        match = re.search(pattern, ocr_text, re.IGNORECASE)

        if match:
            date_text = match.group(1)

            for fmt in ("%m/%d/%Y", "%m-%d-%Y"):
                try:
                    expiry_date = datetime.strptime(
                        date_text,
                        fmt
                    ).date()
                    break
                except ValueError:
                    pass

        if expiry_date:
            break

    if expiry_date is None:
        return {
            "status": "NOT FOUND",
            "message": "Expiry date could not be detected."
        }

    today = datetime.now().date()

    if expiry_date < today:
        return {
            "status": "EXPIRED",
            "message": "Document expiry date has already passed."
        }

    return {
        "status": "VALID",
        "message": "Document expiry date is currently valid."
    }


# Upload document
doc_file = st.file_uploader(
    "Upload identity document (JPG/PNG)",
    type=["jpg", "jpeg", "png"]
)

person_file = st.file_uploader(
    "Upload person photo (optional)",
    type=["jpg", "jpeg", "png"]
)


if doc_file:

    doc_img = Image.open(doc_file).convert("RGB")

    st.image(
        doc_img,
        caption="Uploaded Document",
        width=520
    )

    if st.button("🔎 Verify Document", type="primary"):

        with st.spinner("Running screening pipeline..."):

            image_np = np.array(doc_img)

            # OCR
            ocr_text = extract_text(image_np)

            # Document validation
            validation = validate_document(ocr_text)

            # Tamper detection
            tamper = detect_tamper(image_np)

            # Expiry check
            expiry = check_expiry(ocr_text)

            # Face verification
            face = {
                "status": "Not checked",
                "score": 0.0,
                "message": "Upload a person photo to run face comparison."
            }

            if person_file:

                person_img = Image.open(person_file).convert("RGB")

                face = verify_face(
                    image_np,
                    np.array(person_img)
                )

            # Final consistency
            final = consistency_result(
                validation,
                tamper,
                face
            )
            # Simple rule-based authenticity screening

            if expiry["status"] == "EXPIRED":
             authenticity = "SUSPICIOUS / EXPIRED"

            elif validation["status"] != "PASS":
             authenticity = "SUSPICIOUS / POSSIBLE FAKE"

            elif "NO STRONG ANOMALY" not in tamper["status"].upper():
             authenticity = "SUSPICIOUS / POSSIBLE FAKE"

            else:
             authenticity = "LIKELY REAL"

        # Decide displayed result
        display_risk = final["risk"]

        if expiry["status"] == "EXPIRED":
            display_risk = "EXPIRED"

        elif expiry["status"] == "NOT FOUND":
            if display_risk == "VALID":
                display_risk = "EXPIRY NOT VERIFIED"


        st.divider()

        # Result box
        st.subheader("🔐 Identity Screening Result")

        if authenticity == "LIKELY REAL":
         st.success("🟢 LIKELY REAL")

        else:
         st.error("🔴 " + authenticity)

        # Metrics
        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Risk Result",
            display_risk
        )

        c2.metric(
            "Tamper Score",
            f'{tamper["score"]:.2f}'
        )

        c3.metric(
            "Face Check",
            face["status"]
        )


        # Extracted information
        st.subheader("Extracted Information")

        st.code(
            ocr_text
            if ocr_text.strip()
            else "No readable text detected."
        )


        # Verification details
        st.subheader("Verification Details")

        st.write(
            "• Document validation:",
            validation["status"]
        )

        st.write(
            "• Expiry check:",
            expiry["status"]
        )

        st.write(
            "• Expiry information:",
            expiry["message"]
        )

        st.write(
            "• Tamper/anomaly check:",
            tamper["status"]
        )

        st.write(
            "• Face verification:",
            face["message"]
        )

        st.write(
            "• Consistency check:",
            final["consistency"]
        )


        # Evidence
        st.subheader("Evidence / Reason")

        for reason in final["reasons"]:
            st.write("•", reason)

        if expiry["status"] == "EXPIRED":

            st.write(
                "• Document expiry date has already passed."
            )

        elif expiry["status"] == "VALID":

            st.write(
                "• Document expiry date is currently valid."
            )

        else:

            st.write(
                "• Expiry date could not be verified from OCR."
            )


        st.info(
            "Prototype decision-support output. "
            "Final verification should be performed by an authorized human reviewer."
        )


else:

    st.info("Upload a document to begin.")