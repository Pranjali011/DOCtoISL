import cv2
import numpy as np
import pytesseract
from pytesseract import Output


def extract_text_from_image(file_bytes: bytes) -> str:
    """
    Extract text from an image using Tesseract OCR.
    Supports JPG, JPEG, PNG.
    Includes preprocessing for better OCR accuracy.
    """

    try:
        # Load image from bytes
        np_img = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        if img is None:
            return ""

        # Preprocessing 
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Remove noise
        gray = cv2.medianBlur(gray, 3)

        # Adaptive threshold for variable lighting
        bin_img = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31, 2
        )

        # Dilation & erosion for thicker text
        kernel = np.ones((2, 2), np.uint8)
        bin_img = cv2.erode(bin_img, kernel, iterations=1)
        bin_img = cv2.dilate(bin_img, kernel, iterations=1)

        # OCR Extraction
        custom_config = r"--oem 3 --psm 6"  
        text = pytesseract.image_to_string(bin_img, config=custom_config)


        # Cleanup text
        clean_text = " ".join(text.split())

        return clean_text

    except Exception as e:
        print(f"[OCR ERROR] {e}")
        return ""
