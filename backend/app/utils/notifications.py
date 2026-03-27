import smtplib
from email.mime.text import MIMEText


# =========================
# EMAIL SERVICE
# =========================
def send_email(email, subject, body):

    sender_email = "awaresakshi331@gmail.com"
    sender_password = "pohzcxkttbfgdsrs"   # Gmail App Password

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = email

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()

        print("✅ Email sent to:", email)

    except Exception as e:
        print("❌ Email sending failed:", e)


# =========================
# SMS SERVICE (DEMO MODE)
# =========================
def send_sms(phone, message):

    # Demo SMS (no Twilio required)
    print("\n📱 SMS SENT")
    print("To:", phone)
    print("Message:", message)