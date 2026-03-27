import cv2
import numpy as np

def preprocess_image(image_path):
    """
    Advanced preprocessing for OCR
    """

    img = cv2.imread(image_path)

    if img is None:
        raise ValueError(f"Cannot read image at {image_path}")

    # Resize for better OCR
    img = cv2.resize(img, None, fx=2, fy=2)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Remove noise
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    # Sharpen image
    kernel = np.array([[0,-1,0],
                       [-1,5,-1],
                       [0,-1,0]])
    sharp = cv2.filter2D(blur, -1, kernel)

    # Threshold
    thresh = cv2.threshold(
        sharp,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    # Morphological closing to strengthen text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    return morph