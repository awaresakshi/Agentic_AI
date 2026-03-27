import re


def verify_pan(pan):

    if not pan:
        return {
            "score": 0.1,
            "status": "invalid",
            "reason": "PAN not provided"
        }

    pan = pan.strip().upper()

    pattern = r"^[A-Z]{5}[0-9]{4}[A-Z]$"

    if re.fullmatch(pattern, pan):

        print("PAN VERIFIED:", pan)

        return {
            "score": 0.95,
            "status": "valid",
            "pan_number": pan,
            "reason": "Valid PAN format"
        }

    print("PAN INVALID:", pan)

    return {
        "score": 0.3,
        "status": "invalid",
        "pan_number": pan,
        "reason": "Invalid PAN format"
    }