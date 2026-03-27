class DecisionEngine:

    def evaluate(self, pan_result, aadhaar_result, face_result, fraud_result):

        pan_score = pan_result.get("score", 0)
        aadhaar_score = aadhaar_result.get("score", 0)
        face_score = face_result.get("score", 0)
        fraud_score = fraud_result.get("score", 0)

        # Weighted trust score
        trust_score = (
            pan_score * 0.3 +
            aadhaar_score * 0.3 +
            face_score * 0.3 +
            (1 - fraud_score) * 0.1
        )

        # 🧠 Detailed agent reasons
        details = []

        if pan_score >= 0.8:
            details.append("PAN verified successfully")
        elif pan_score >= 0.5:
            details.append("PAN partially matched")
        else:
            details.append("PAN verification failed")

        if aadhaar_score >= 0.8:
            details.append("Aadhaar verified successfully")
        elif aadhaar_score >= 0.5:
            details.append("Aadhaar partially matched")
        else:
            details.append("Aadhaar verification failed")

        if face_score >= 0.8:
            details.append("Face matched correctly")
        elif face_score >= 0.5:
            details.append("Face match uncertain")
        else:
            details.append("Face verification failed")

        if fraud_score <= 0.3:
            details.append("No fraud risk detected")
        elif fraud_score <= 0.6:
            details.append("Moderate fraud risk")
        else:
            details.append("High fraud risk detected")

        # 🎯 Decision logic
        if trust_score >= 0.75:
            decision = "APPROVED"
            reason = "All verifications passed successfully"

        elif trust_score >= 0.55:
            decision = "UNDER_REVIEW"
            reason = "Some checks are uncertain, manual review required"

        else:
            decision = "REJECTED"
            reason = "Multiple verification checks failed"

        return {
            "decision": decision,
            "reason": reason,
            "trust_score": round(trust_score, 2),

            # 🔥 NEW (important for UI)
            "details": details,

            # send scores also (for your dashboard bars)
            "pan_score": pan_score,
            "aadhaar_score": aadhaar_score,
            "face_score": face_score,
            "fraud_score": fraud_score
        }