import jwt
from flask import request, current_app
from datetime import datetime, timedelta


# -------- GENERATE JWT TOKEN --------
def generate_token(user_id, expires_hours=2):

    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=expires_hours)
    }

    token = jwt.encode(
        payload,
        current_app.config.get(
            "SECRET_KEY",
            "banking-ai-kyc-super-secure-secret-key-2026"
        ),
        algorithm="HS256"
    )

    return token


# -------- GET CURRENT USER FROM TOKEN --------
def get_current_user():

    auth_header = request.headers.get("Authorization")

    print("AUTH HEADER:", auth_header)   # ✅ DEBUG

    if not auth_header:
        return None

    parts = auth_header.split(" ")

    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None

    token = parts[1]

    try:
        decoded = jwt.decode(
            token,
            current_app.config.get(
                "SECRET_KEY",
                "banking-ai-kyc-super-secure-secret-key-2026"
            ),
            algorithms=["HS256"]
        )

        print("DECODED:", decoded)   # ✅ DEBUG

        return decoded.get("user_id")

    except jwt.ExpiredSignatureError:
        print("Token expired")
        return None

    except jwt.InvalidTokenError:
        print("Invalid token")
        return None