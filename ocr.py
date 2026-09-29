def extract_text(image):
    # RapidOCR is used when installed. The app remains runnable if OCR is unavailable.
    try:
        from rapidocr_onnxruntime import RapidOCR
        engine = RapidOCR()
        result, _ = engine(image)
        if not result:
            return ""
        return "\n".join([str(item[1]) for item in result])
    except Exception:
        try:
            import pytesseract
            return pytesseract.image_to_string(image)
        except Exception:
            return ""
