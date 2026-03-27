import cv2
import pytesseract
import numpy as np
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class PANAgent:
    def preprocess(self, img):
        """Advanced preprocessing for better OCR"""
        # Resize for small text
        img = cv2.resize(img, None, fx=2.5, fy=2.5)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        
        # Sharpening
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        sharp = cv2.filter2D(gray, -1, kernel)
        
        # Adaptive threshold
        thresh = cv2.adaptiveThreshold(sharp, 255,
                                       cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 15, 3)
        return thresh

    def extract_text(self, img):
        """Run OCR with single tuned config"""
        config = "--oem 3 --psm 6"
        text = pytesseract.image_to_string(img, config=config)
        text = text.upper()
        return text

    def clean_text(self, text):
        """Clean OCR noise"""
        text = re.sub(r"[^A-Z0-9/\n ]", " ", text)
        text = re.sub(r"(\d)\s+(\d)", r"\1\2", text)  # fix digit spacing
        return text

    def verify(self, image_path):
        try:
            img = cv2.imread(image_path)
            if img is None:
                return {"pan_number": None, "name": None, "dob": None, "score": 0.0, "status": "image_not_readable"}
            
            processed = self.preprocess(img)
            text = self.extract_text(processed)
            text = self.clean_text(text)
            
            # PAN detection
            pan_match = re.search(r"[A-Z]{5}[0-9]{4}[A-Z]", text)
            pan_number = pan_match.group() if pan_match else None
            
            # DOB detection (improved regex)
            dob_match = re.search(r"\d{2}[-/ ]\d{2}[-/ ]\d{4}", text)
            dob = dob_match.group() if dob_match else None
            
            # Name detection (improved)
            name = None
            for line in text.split("\n"):
                line = line.strip()
                if len(line.split()) >= 2 and not re.search(r"\d", line):
                    if all(k not in line for k in ["INCOME", "TAX", "DEPARTMENT", "GOVT", "INDIA"]):
                        name = line
                        break
            
            # Fallback: pick first valid multi-word string
            if not name:
                names = re.findall(r"[A-Z]{2,}(?: [A-Z]{2,})?", text)
                if names:
                    name = names[0]
            
            # Scoring
            score = 0
            if pan_number: score += 0.5
            if name: score += 0.3
            if dob: score += 0.2
            status = "valid" if score >= 0.7 else "partial"
            
            return {"pan_number": pan_number, "name": name, "dob": dob, "score": round(score, 2), "status": status}
        except Exception as e:
            return {"pan_number": None, "name": None, "dob": None, "score": 0.0, "status": "error", "error": str(e)}