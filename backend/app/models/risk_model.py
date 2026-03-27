from backend.app.db import db
from datetime import datetime

class RiskApplication(db.Model):
    __tablename__ = "risk_applications"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))

    risk_score = db.Column(db.Integer)
    decision = db.Column(db.String(20))
    reason = db.Column(db.Text)

    kyc_result = db.Column(db.JSON)
    fraud_result = db.Column(db.JSON)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)