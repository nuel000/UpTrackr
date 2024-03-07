from email.message import EmailMessage
import ssl
import smtplib
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
email_password = os.environ.get("MY_PASSWORD")



def send_mail(email_receiver,body):
    email_sender =  'thedatadude000@gmail.com'
    email_password = os.environ.get("MY_PASSWORD")

    email_receiver = f'{email_receiver}'
    receiver_name = 'UpTrackr'  
    subject = 'New Job Alert'
    em = EmailMessage()
    em['From'] = f'{receiver_name} <{email_sender}>'  # Custom name and email
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(em)
        


