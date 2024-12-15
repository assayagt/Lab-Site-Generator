import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.main.Util.ExceptionsEnum import ExceptionsEnum

class EmailNotification:
    def __init__(self, recipient, subject, body):
        self.recipient = recipient
        self.subject = subject
        self.body = body

    def send_email(self):
        # define sender email and the server
        #TODO: Change those detils:
        sender_email = "your_email@example.com"
        password = "your_password"
        smtp_server = "smtp.example.com"
        smtp_port = 587

        # define message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = self.recipient
        msg['Subject'] = self.subject
        msg.attach(MIMEText(self.body, 'plain'))

        # send the mail
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # start TLS
                server.login(sender_email, password)
                server.sendmail(sender_email, self.recipient, msg.as_string())
        except Exception as e:
            raise Exception(ExceptionsEnum.ERROR_SENDING_EMAIL)
