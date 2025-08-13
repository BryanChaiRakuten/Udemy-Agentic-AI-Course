from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
load_dotenv(override=True)


# when you set up a custom tool you have to first describe using a pedantic object, the schema of what will be passed in to your
# custom tool.
# And then you end up writing an underscore run method, which is going to take that schema as its parameters.

# TODO
# Mimic push but send to my email

class PushNotification(BaseModel):
    """A message to be sent to the user"""
    message: str = Field(..., description="The message to be sent to the user.")

class PushNotificationTool(BaseTool):
    
    name: str = "Send a Push Notification"
    description: str = (
        "This tool is used to send a push notification to the user."
    )
    # what kind of arguments needed to pass in
    args_schema: Type[BaseModel] = PushNotification

    # # message parameter corresponds to the message field in the PushNotification schema
    # def _run(self, message: str) -> str:
        
    #     pushover_user = os.getenv("PUSHOVER_USER")
    #     pushover_token = os.getenv("PUSHOVER_TOKEN")
    #     pushover_url = "https://api.pushover.net/1/messages.json"
        
    #     print(f"Push: {message}")
    #     payload = {"user": pushover_user, "token": pushover_token, "message": message}
    #     requests.post(pushover_url, data=payload)
    #     return '{"notification": "ok"}'
    
    # message parameter corresponds to the message field in the PushNotification schema
    def _run(self, message: str) -> str:
        
        gmail_user = os.getenv("GMAIL_EMAIL")
        app_password = os.getenv("GMAIL_APP_PASSWORD")
        to_email = os.getenv("GMAIL_TO_EMAIL")
        print(f"Using Gmail user: {gmail_user}")
        print(f"Using recipient email: {to_email}")

        # Email content
        subject = 'Stock picker'
        body = message

        
        print(f"Push: {message}")
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
        