import joblib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, "models", "fraud_model.pkl")

model = None

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
    print("✅ Fraud model loaded successfully")
else:
    print("❌ Fraud model not found")


def check_fraud(data):

    age = int(data.get("age", 0))
    income = int(data.get("income", 0))
    credit_score = int(data.get("credit_score", 600))

    pan_valid = data.get("pan_valid", False)
    aadhaar_valid = data.get("aadhaar_valid", False)
    face_match = data.get("face_match", False)

    signals = []

    # Identity signals
    if not pan_valid:
        signals.append("PAN invalid")

    if not aadhaar_valid:
        signals.append("Aadhaar invalid")

    if not face_match:
        signals.append("Face mismatch")

    # Financial signals
    if credit_score < 500:
        signals.append("Very low credit score")

    if age < 21 and income > 500000:
        signals.append("Age-income mismatch")

    if income > 2000000:
        signals.append("Unusually high income")

    # ML prediction
    if model:
        try:
            features = [[age, income, credit_score]]
            probability = model.predict_proba(features)[0][1]
        except:
            probability = 0.5
    else:
        probability = 0.5

    fraud_score = round(probability, 2)

    # Confidence level
    if fraud_score > 0.75:
        risk = "High fraud risk"
        confidence = "High"

    elif fraud_score > 0.45:
        risk = "Medium fraud risk"
        confidence = "Medium"

    else:
        risk = "Low fraud risk"
        confidence = "High"

    return {
        "score": fraud_score,
        "risk_level": risk,
        "confidence": confidence,
        "signals": signals
    }