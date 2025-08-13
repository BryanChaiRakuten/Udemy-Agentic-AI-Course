import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
load_dotenv(override=True)

# Gmail credentials
# gmail_user = 'bryanchat98@gmail.com'
# app_password = 'pikp wyen ahnf cfty'  # 16-character App Password
# to_email = "hibyeloveu@gmail.com"
gmail_user = os.getenv("GMAIL_EMAIL")
app_password = os.getenv("GMAIL_APP_PASSWORD")
to_email = os.getenv("GMAIL_TO_EMAIL")

print(f"Using Gmail user: {gmail_user}")
print(f"Using recipient email: {to_email}")


# Email content
subject = 'Hello from Python'
body = 'This is a test email sent from Python using Gmail.'

# Construct email
msg = MIMEMultipart()
msg['From'] = gmail_user
msg['To'] = to_email
msg['Subject'] = subject
msg.attach(MIMEText(body, 'plain'))

try:
    # Connect to Gmail SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_user, app_password)
    server.send_message(msg)
    server.quit()
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")
