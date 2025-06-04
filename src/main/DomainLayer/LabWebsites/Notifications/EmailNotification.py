import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.DAL.DTOs.Notification_dto import notification_dto

# Define the required Gmail API scope
sender_email = "notifications.lab.website@gmail.com"

smtp_server = "smtp.gmail.com"
smtp_port = 587
login = sender_email
password = "ijtb kvpg efep srbu"

# HTML email template with embedded SVG logo (base64)
EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .email-container {
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            padding: 30px;
        }
        .logo {
            display: block;
            margin: 0 auto 20px auto;
            width: 80px;
        }
        .header {
            background-color: #3498db;
            color: white;
            padding: 20px;
            border-radius: 8px 8px 0 0;
            margin: -30px -30px 20px -30px;
        }
        .content {
            padding: 20px 0;
        }
        .footer {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            font-size: 12px;
            color: #666;
        }
        .button {
            display: inline-block;
            padding: 12px 24px;
            background-color: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            margin-top: 20px;
        }
        .button:hover {
            background-color: #2980b9;
        }
    </style>
</head>
<body>
    <div class=\"email-container\">
        <img class=\"logo\" src=\"data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAwIiBoZWlnaHQ9IjEwMCIgdmlld0JveD0iMCAwIDEwMCAxMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3QgeD0iMTAiIHk9IjIwIiB3aWR0aD0iODAiIGhlaWdodD0iNjAiIHJ4PSI4IiBmaWxsPSIjMjIyIiBzdHJva2U9IiNiYmIiIHN0cm9rZS13aWR0aD0iMyIvPjxjaXJjbGUgY3g9IjI1IiBjeT0iMzIiIHI9IjMiIGZpbGw9IiNiYmIiLz48cmVjdCB4PSIzNSIgeT0iMjkiIHdpZHRoPSI1MCIgaGVpZ2h0PSI2IiByeD0iMiIgZmlsbD0iIzQ0NCIvPjxwYXRoIGQ9Ik01MCA0MCBMNjAgNzAgQTEwIDEwIDAgMCAxIDQwIDcwIFoiIGZpbGw9IiNiMzlkZGIiIHN0cm9rZT0iI2ZmZiIgc3Ryb2tlLXdpZHRoPSIyIi8+PGVsbGlwc2UgY3g9IjUwIiBjeT0iNjAiIHJ4PSIzIiByeT0iMiIgZmlsbD0iI2ZmZiIgb3BhY2l0eT0iMC41Ii8+PC9zdmc+\" alt=\"Lab Website Logo\" />
        <div class=\"header\">
            <h2>{subject}</h2>
        </div>
        <div class=\"content\">
            {body}
        </div>
        <div class=\"footer\">
            <p>This is an automated message from Lab Website Generator.</p>
            <p>Please do not reply to this email.</p>
        </div>
    </div>
</body>
</html>
"""

class EmailNotification:
    def __init__(self, id, recipient, subject, body, domain, request_email=None, publication_id=None):
        self.id = id  # Generate a unique ID for the notification
        self.recipient = recipient
        self.subject = subject
        self.body = body
        self.request_email = request_email
        self.publication_id = publication_id
        self.isRead = False
        self.domain = domain

    def send_email(self):
        """Authenticate and send the email with HTML formatting."""
        # Create the email components
        message = MIMEMultipart('alternative')
        message['From'] = sender_email
        message['To'] = self.recipient
        message['Subject'] = self.subject

        # Create both plain text and HTML versions
        text_plain = self.body
        text_html = EMAIL_TEMPLATE.format(
            subject=self.subject,
            body=self.body.replace('\n', '<br>')  # Convert newlines to HTML breaks
        )

        # Attach both versions
        part1 = MIMEText(text_plain, 'plain')
        part2 = MIMEText(text_html, 'html')

        message.attach(part1)
        message.attach(part2)

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
            domain=self.domain,  # Domain is not applicable for email notifications
            id=self.id,
            recipient=self.recipient,
            subject=self.subject,
            body=self.body,
            request_email=self.request_email,
            publication_id=self.publication_id,
            isRead=self.isRead
        )