import face_recognition
import cv2
import numpy as np


def enhance_image(img):
    """Light enhancement without breaking face features"""

    # Keep RGB (IMPORTANT)
    img = cv2.resize(img, None, fx=1.2, fy=1.2)

    # Improve contrast only
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)

    l = cv2.equalizeHist(l)

    lab = cv2.merge((l, a, b))
    img = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)

    return img


def get_best_face_encoding(image):
    """Detect largest face"""

    locations = face_recognition.face_locations(image, model="hog")

    if len(locations) == 0:
        return None

    # correct area calculation
    def area(box):
        top, right, bottom, left = box
        return (bottom - top) * (right - left)

    best_face = max(locations, key=area)

    encodings = face_recognition.face_encodings(image, [best_face])

    if not encodings:
        return None

    return encodings[0]


def verify_face(selfie_path, pan_path):

    try:
        # ✅ Load images (RGB already)
        selfie = face_recognition.load_image_file(selfie_path)
        pan = face_recognition.load_image_file(pan_path)

        # ✅ Enhance safely
        selfie = enhance_image(selfie)
        pan = enhance_image(pan)

        # ✅ Get encodings
        selfie_enc = get_best_face_encoding(selfie)
        pan_enc = get_best_face_encoding(pan)

        if selfie_enc is None or pan_enc is None:
            return {
                "match": False,
                "score": 0.0,
                "reason": "Face not detected"
            }

        # ✅ Distance
        distance = face_recognition.face_distance([selfie_enc], pan_enc)[0]

        # ✅ Convert to similarity
        score = max(0, 1 - distance)

        print("\n===== FACE DEBUG =====")
        print("Distance:", distance)
        print("Score:", score)
        print("======================\n")

        # ✅ Better threshold
        if distance < 0.55:
            return {
                "match": True,
                "score": round(score, 2),
                "reason": "Face matched"
            }

        return {
            "match": False,
            "score": round(score, 2),
            "reason": "Face mismatch"
        }

    except Exception as e:
        return {
            "match": False,
            "score": 0.0,
            "reason": str(e)
        }