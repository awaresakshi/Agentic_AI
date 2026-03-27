from flask import Blueprint, jsonify, request, current_app
import jwt, datetime
from functools import wraps
import pymysql

admin_bp = Blueprint("admin_bp", __name__)
SECRET_KEY = "admin_secret_key_123456789_strong"  # separate key for admin


# ---------------- DB CONNECTION ----------------
def get_db():
    return pymysql.connect(
        host=current_app.config["MYSQL_HOST"],
        user=current_app.config["MYSQL_USER"],
        password=current_app.config["MYSQL_PASSWORD"],
        database=current_app.config["MYSQL_DB"],
        cursorclass=pymysql.cursors.DictCursor
    )


# ---------------- ADMIN LOGIN ----------------
@admin_bp.route("/login", methods=["POST"])
def admin_login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "admin123":
        token = jwt.encode({
            "admin": True,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token})

    return jsonify({"message": "Invalid credentials"}), 401


# ---------------- TOKEN PROTECTION ----------------
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth or not auth.lower().startswith("bearer "):
            return jsonify({"message": "Token missing"}), 403

        token = auth.split(" ")[1]
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({"message": "Invalid token"}), 403

        return f(*args, **kwargs)
    return decorated


# ---------------- GET ALL UNDER REVIEW APPLICATIONS ----------------
@admin_bp.route("/applications", methods=["GET"])
@admin_required
def get_applications():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT * FROM applications
        WHERE status='under_review'
        ORDER BY created_at DESC
    """)
    applications = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(applications)


# ---------------- APPROVE / REJECT APPLICATION ----------------
@admin_bp.route("/applications/<int:id>", methods=["PUT"])
@admin_required
def update_application(id):
    data = request.json
    decision = data.get("decision")
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE applications
        SET decision=%s, status='completed'
        WHERE id=%s
    """, (decision, id))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Application updated successfully"})