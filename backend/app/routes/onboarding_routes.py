from flask import Blueprint, request, jsonify, current_app
import os, uuid, pymysql
from datetime import datetime
from app.agents.pan_agent import PANAgent
from app.agents.aadhaar_agent import verify_aadhaar
from app.agents.face_agent import verify_face
from app.agents.fraud_agent import check_fraud
from app.agents.decision_engine import DecisionEngine
from app.utils.file_utils import allowed_file
from app.utils.image_hash import generate_image_hash
from app.utils.jwt_utils import get_current_user

onboarding_bp = Blueprint("onboarding_bp", __name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_db():
    return pymysql.connect(
        host=current_app.config["MYSQL_HOST"],
        user=current_app.config["MYSQL_USER"],
        password=current_app.config["MYSQL_PASSWORD"],
        database=current_app.config["MYSQL_DB"],
        cursorclass=pymysql.cursors.DictCursor
    )

# --------------------------
# Helper to safely default None
# --------------------------
def safe(val, default=""):
    return val if val is not None else default

# =========================
# APPLY ACCOUNT
# =========================
@onboarding_bp.route("/apply", methods=["POST"])
def apply():
    try:
        # 🔐 USER AUTH
        user_id = get_current_user()
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        # =========================
        # FORM DATA
        # =========================
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        age = int(request.form.get("age") or 0)
        income = float(request.form.get("income") or 0)
        credit_score = int(request.form.get("credit_score") or 600)
        account_type = request.form.get("account_type", "saving")
        dob_input = request.form.get("dob")
        address = request.form.get("address")
        occupation = request.form.get("occupation")

        # =========================
        # FILES
        # =========================
        pan_file = request.files.get("pan_card")
        aadhaar_file = request.files.get("aadhaar")
        selfie_file = request.files.get("selfie")

        for f, name in [(pan_file, "PAN"), (aadhaar_file, "Aadhaar"), (selfie_file, "Selfie")]:
            if not f or not allowed_file(f.filename):
                return jsonify({"error": f"Invalid {name} file"}), 400

        # =========================
        # SAVE FILES
        # =========================
        pan_filename = str(uuid.uuid4()) + "_" + pan_file.filename
        aadhaar_filename = str(uuid.uuid4()) + "_" + aadhaar_file.filename
        selfie_filename = str(uuid.uuid4()) + "_" + selfie_file.filename

        pan_path = os.path.join(UPLOAD_FOLDER, pan_filename)
        aadhaar_path = os.path.join(UPLOAD_FOLDER, aadhaar_filename)
        selfie_path = os.path.join(UPLOAD_FOLDER, selfie_filename)

        pan_file.save(pan_path)
        aadhaar_file.save(aadhaar_path)
        selfie_file.save(selfie_path)

        # =========================
        # DOB FORMAT
        # =========================
        dob = None
        if dob_input:
            try:
                dob = datetime.strptime(dob_input.strip(), "%d/%m/%Y").strftime("%Y-%m-%d")
            except:
                dob = None

        # =========================
        # AI PROCESSING
        # =========================
        pan_hash = generate_image_hash(pan_path)
        aadhaar_hash = generate_image_hash(aadhaar_path)

        pan_result = safe(PANAgent().verify(pan_path), {})
        aadhaar_result = safe(verify_aadhaar(aadhaar_path), {})
        face_result = safe(verify_face(selfie_path, aadhaar_path), {})
        fraud_result = safe(check_fraud({
            "age": age,
            "income": income,
            "credit_score": credit_score
        }), {})

        engine = DecisionEngine()
        result = safe(engine.evaluate(pan_result, aadhaar_result, face_result, fraud_result), {})

        decision = safe(result.get("decision"), "UNDER_REVIEW")
        reason = safe(result.get("reason"), "")

        status = "under_review" if decision == "UNDER_REVIEW" else "completed"

        # =========================
        # DB INSERT
        # =========================
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO applications
            (user_id, account_type, full_name, email, phone, dob, age,
             pan, aadhaar, income, address, occupation,
             pan_score, aadhaar_score, face_score, fraud_score,
             pan_image_hash, aadhaar_image_hash,
             status, decision, reason)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                    %s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            safe(user_id, 0),
            safe(account_type),
            safe(full_name),
            safe(email),
            safe(phone),
            safe(dob),
            safe(age, 0),
            safe(pan_result.get("pan_number")),
            safe(aadhaar_result.get("aadhaar_number")),
            safe(income, 0),
            safe(address),
            safe(occupation),
            safe(pan_result.get("score", 0), 0),
            safe(aadhaar_result.get("score", 0), 0),
            safe(face_result.get("score", 0), 0),
            safe(fraud_result.get("score", 0), 0),
            safe(pan_hash),
            safe(aadhaar_hash),
            safe(status),
            safe(decision),
            safe(reason)
        ))

        application_id = cursor.lastrowid
        db.commit()
        cursor.close()
        db.close()
        return jsonify({
           "message": "Application submitted successfully",
         "application": {
        "account_type": account_type,
        "decision": decision,
        "reason": reason,
        "pan_score": pan_result.get("score", 0),
        "aadhaar_score": aadhaar_result.get("score", 0),
        "face_score": face_result.get("score", 0),
        "fraud_score": fraud_result.get("score", 0)
    }
}), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500