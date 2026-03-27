# app/db.py
import pymysql
from flask import current_app

# ---------------- CONFIG ----------------
class Config:
    SECRET_KEY = "banking-ai-kyc-super-secure-secret-key-2026"

    MYSQL_HOST = "127.0.0.1"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "sakshi@123"
    MYSQL_DB = "agentic_ai"  # Make sure this database exists in MySQL
    MYSQL_PORT = 3306
    MYSQL_CURSORCLASS = "DictCursor"

    UPLOAD_FOLDER = "uploads/"

# ---------------- DB CONNECTION ----------------
def get_db():
    return pymysql.connect(
        host=current_app.config["MYSQL_HOST"],
        user=current_app.config["MYSQL_USER"],
        password=current_app.config["MYSQL_PASSWORD"],
        database=current_app.config["MYSQL_DB"],
        cursorclass=pymysql.cursors.DictCursor
    )