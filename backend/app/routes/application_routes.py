from flask import Blueprint, jsonify
from app.db import get_db

applications_bp = Blueprint("applications_bp", __name__)

@applications_bp.route("/applications", methods=["GET"])
def get_applications():
    try:
        db = get_db()
        cur = db.cursor()

        query = """
        SELECT a.*, d.pan_file, d.aadhaar_file, d.selfie_file, f.fraud_score
        FROM applications a
        LEFT JOIN documents d ON a.id = d.application_id
        LEFT JOIN fraud_results f ON a.id = f.application_id
        ORDER BY a.id DESC
        """

        cur.execute(query)
        results = cur.fetchall()

        cur.close()
        db.close()

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500