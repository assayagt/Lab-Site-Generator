import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Define the required Gmail API scope
sender_email = "notifications.lab.website@gmail.com"

smtp_server = "smtp.gmail.com"
smtp_port = 587
login = sender_email
password = "ijtb kvpg efep srbu"


class EmailNotification:
    def __init__(self, recipient, subject, body):
        self.recipient = recipient
        self.subject = subject
        self.body = body

    def send_email(self):
        """Authenticate and send the email."""
        # Create the email components
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = self.recipient
        message['Subject'] = self.subject

        # Email body (plain text)
        message.attach(MIMEText(self.body, 'plain'))

        # Connect and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(login, password)
        server.sendmail(sender_email, self.recipient, message.as_string())
        server.quit()