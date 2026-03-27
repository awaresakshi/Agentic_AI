import cv2
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def verify_aadhaar(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None:
            return {"aadhaar_number": None, "name": None, "dob": None, "score": 0.1, "status": "image_not_readable"}
        
        # Resize & grayscale
        img = cv2.resize(img, None, fx=2.5, fy=2.5)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 15, 3)
        
        text = pytesseract.image_to_string(thresh)
        text = text.upper().replace("O", "0").replace("I", "1").replace("L", "1").replace("B", "8")
        text = re.sub(r"(\d)\s+(\d)", r"\1\2", text)
        
        # Aadhaar number
        aadhaar_match = re.search(r"\d{4}\s?\d{4}\s?\d{4}", text)
        aadhaar_number = aadhaar_match.group().replace(" ", "") if aadhaar_match else None
        
        # DOB detection
        dob_match = re.search(r"\d{2}[-/ ]\d{2}[-/ ]\d{4}", text)
        dob = dob_match.group() if dob_match else None
        
        # Name detection
        name = None
        for line in text.split("\n"):
            line = line.strip()
            if len(line.split()) >= 2 and not re.search(r"\d", line):
                if all(k not in line for k in ["GOVERNMENT", "INDIA"]):
                    name = line
                    break
        # Fallback
        if not name:
            names = re.findall(r"[A-Z]{2,}(?: [A-Z]{2,})?", text)
            if names:
                name = names[0]
        
        # Scoring
        score = 0
        if aadhaar_number: score += 0.6
        if name: score += 0.2
        if dob: score += 0.2
        status = "valid" if score > 0.5 else "partial"
        
        return {"aadhaar_number": aadhaar_number, "name": name, "dob": dob, "score": round(score, 2), "status": status}
    
    except Exception as e:
        return {"aadhaar_number": None, "name": None, "dob": None, "score": 0, "status": "error", "error": str(e)}