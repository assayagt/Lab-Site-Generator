import smtplib
import uuid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.DAL.DTOs.Notification_dto import notification_dto

# Define the required Gmail API scope
sender_email = "notifications.lab.website@gmail.com"

smtp_server = "smtp.gmail.com"
smtp_port = 587
login = sender_email
password = "ijtb kvpg efep srbu"


class EmailNotification:
    def __init__(self, recipient, subject, body, domain, request_email=None, publication_id=None):
        self.id = str(uuid.uuid4())  # Generate a unique ID for the notification
        self.recipient = recipient
        self.subject = subject
        self.body = body
        self.request_email = request_email
        self.publication_id = publication_id
        self.isRead = False
        self.doamin = domain

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

    def get_is_read(self):
        return self.isRead

    #get subject
    def get_subject(self):
        return self.subject

    #get body
    def get_body(self):
        return self.body

    def to_dict(self):
        """Convert the notification to a dictionary for easy JSON conversion."""
        return {
            "id": self.id,
            "subject": self.subject,
            "body": self.body
        }

    def mark_as_read(self):
        """Mark the notification as read."""
        self.isRead = True

    def get_request_email(self):
        return self.request_email

    def to_dto(self):
        """Convert the notification to a DTO for database storage."""
        return notification_dto(
            domain=self.doamin,  # Domain is not applicable for email notifications
            id=self.id,
            recipient=self.recipient,
            subject=self.subject,
            body=self.body,
            request_email=self.request_email,
            publication_id=self.publication_id,
            isRead=self.isRead
        )