from twilio.rest import Client

def send_sms(phone, message):
    account_sid = 'your_twilio_sid'
    auth_token = 'your_twilio_auth_token'
    from_number = '+1234567890'  # your Twilio number

    client = Client(account_sid, auth_token)
    try:
        client.messages.create(
            body=message,
            from_=from_number,
            to=phone
        )
        print(f"SMS sent to {phone}")
    except Exception as e:
        print("SMS sending failed:", e)