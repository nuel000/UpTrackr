import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendmail(recipient,body):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'thedatadude000@gmail.com'
    smtp_password = 'XXX XXX XXX'

    # Custom "From" address
    custom_address = 'Uptrackr.com <noreply@uptrackr.com>'

    # Email configuration
    sender = custom_address
    recipient = f'{recipient}'
    subject = 'New Job Notification'
    body = f"{body}"

    # Create message
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    print("Sending...")

    # Establish a connection to the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        # Start TLS for security
        server.starttls()
        # Login to the email account
        server.login(smtp_username, smtp_password)
        # Send the email
        server.sendmail(sender, recipient, message.as_string())

    print('Email sent successfully!')
