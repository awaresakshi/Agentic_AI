from flask import Blueprint, jsonify
from app.db import get_db
from app.utils.jwt_utils import get_current_user

dashboard_bp = Blueprint("dashboard", __name__)

# ---------------- USER PROFILE ----------------
@dashboard_bp.route("/profile", methods=["GET"])
def get_profile():
    user_id = get_current_user()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "SELECT name,email,phone,created_at FROM users WHERE id=%s", (user_id,)
    )
    user = cur.fetchone()
    cur.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "name": user["name"],
        "email": user["email"],
        "phone": user["phone"],
        "created_at": str(user["created_at"]) if user["created_at"] else None
    })


# ---------------- USER APPLICATIONS ----------------
@dashboard_bp.route("/applications", methods=["GET"])
def get_user_applications():
    user_id = get_current_user()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    db = get_db()
    cur = db.cursor()   
    cur.execute("""
        SELECT account_type, decision, status, reason, pan_score, aadhaar_score, face_score, fraud_score, created_at
        FROM applications
        WHERE user_id=%s
        ORDER BY created_at DESC
    """, (user_id,))
    applications = cur.fetchall()
    cur.close()

    result = []
    for app in applications:
        result.append({
            "account_type": app["account_type"],
            "decision": app["decision"],
            "status": app["status"],
            "reason": app["reason"],
            "pan_score": app["pan_score"],
            "aadhaar_score": app["aadhaar_score"],
            "face_score": app["face_score"],
            "fraud_score": app["fraud_score"],
            "created_at": str(app["created_at"])
        })
    return jsonify(result)