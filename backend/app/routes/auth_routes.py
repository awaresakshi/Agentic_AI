from flask import Blueprint, request, jsonify
from app.db import get_db
from app.utils.jwt_utils import generate_token
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

# -------- REGISTER --------
@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json() or {}

        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        password = data.get("password")

        if not all([name, email, phone, password]):
            return jsonify({"message": "All fields are required"}), 400

        db = get_db()
        cur = db.cursor()

        cur.execute("SELECT id FROM users WHERE email=%s", (email,))
        if cur.fetchone():
            cur.close()
            db.close()
            return jsonify({"message": "User already exists"}), 400

        hashed_password = generate_password_hash(password)

        cur.execute(
            "INSERT INTO users (name,email,phone,password) VALUES (%s,%s,%s,%s)",
            (name, email, phone, hashed_password)
        )

        db.commit()
        cur.close()
        db.close()

        return jsonify({"message": "Registration successful"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------- LOGIN --------
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json() or {}

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"message": "Email and password required"}), 400

        db = get_db()
        cur = db.cursor()

        cur.execute("SELECT id, name, password, role FROM users WHERE email=%s", (email,))
        user = cur.fetchone()

        cur.close()
        db.close()

        if not user:
            return jsonify({"message": "User not found"}), 401

        if not check_password_hash(user["password"], password):
            return jsonify({"message": "Invalid password"}), 401

        token = generate_token(user["id"])

        return jsonify({
            "message": "Login successful",
            "token": token,
            "user_id": user["id"],
            "name": user["name"],
            "role": user["role"]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    