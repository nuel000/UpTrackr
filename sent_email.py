import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gmail SMTP server configuration
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'jasperobed@gmail.com'
smtp_password = os.environ.get('SMTP_PASSWORD_ENV_VARIABLE_NAME', '')

# Custom "From" address
custom_address = 'Uptrackr.com <noreply@uptrackr.com>'

# Email configuration
sender = custom_address
recipient = 'momohemmanuel370@gmail.com'
subject = 'New Job Notif'
body = "Hello Senior Dev, 'sent_email.py' file has been created successfully!"

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
