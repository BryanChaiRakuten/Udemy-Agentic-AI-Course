import os
from typing import Dict

import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# @function_tool
# def send_email_template(subject: str, html_body: str) -> Dict[str, str]:
#     """ Send an email with the given subject and HTML body """
#     sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
#     from_email = Email("ed@edwarddonner.com") # put your verified sender here
#     to_email = To("ed.donner@gmail.com") # put your recipient here
#     content = Content("text/html", html_body)
#     mail = Mail(from_email, to_email, subject, content).get()
#     response = sg.client.mail.send.post(request_body=mail)
#     print("Email response", response.status_code)
#     return {"status": "success"}

# workign api
@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """ Send out an email with the given subject and HTML body to all sales prospects """
    # Gmail credentials
    gmail_user = os.getenv("GMAIL_EMAIL")
    app_password =  os.getenv("GMAIL_APP_PASSWORD")

    # Email content
    to_email = 'hibyeloveu@gmail.com'
    # subject = 'Hello tesing email'
    # body = 'This is a test email sent from Python using Gmail.'

    # Construct email
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_body, 'plain'))

    try:
        # Connect to Gmail SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, app_password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
        return {"status": "success"}
    except Exception as e:
        print(f"Failed to send email: {e}")

INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model="gpt-4o-mini",
)
