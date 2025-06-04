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
        """Authenticate and send the email."""
        message = MIMEMultipart("alternative")
        message['From'] = sender_email
        message['To'] = self.recipient
        message['Subject'] = self.subject

        html_body = f"""
        <html>
          <body style="margin: 0; padding: 0; background-color: #f5f5f5;">
            <table align="center" width="100%" cellpadding="0" cellspacing="0" style="background-color: #f5f5f5; padding: 20px;">
              <tr>
                <td>
                  <table align="center" width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                    <!-- Header with Logo -->
                    <tr style="background-color: #cce5ff;">
                      <td style="padding: 20px; text-align: center;">
                        <img src="https://i.postimg.cc/fRKt1LMq/LSGlogo.png" alt="Lab Site Generator" style="max-height: 60px;" />
                      </td>
                    </tr>

                    <!-- Content -->
                    <tr>
                      <td style="padding: 30px;">
                        <h2 style="color: #003366; font-family: Arial, sans-serif; margin-top: 0;">{self.subject}</h2>
                        <p style="font-size: 16px; color: #333333; font-family: Arial, sans-serif; line-height: 1.6;">
                          {self.body}
                        </p>

                        <!-- Button -->
                        <div style="text-align: center; margin-top: 30px;">
                          <a href="http://{self.domain}" style="
                            background-color: #007bff;
                            color: #ffffff;
                            padding: 12px 24px;
                            text-decoration: none;
                            border-radius: 6px;
                            font-size: 16px;
                            font-family: Arial, sans-serif;
                            font-weight: bold;
                            display: inline-block;
                            transition: background-color 0.3s ease, box-shadow 0.3s ease;
                          "
                          onmouseover="this.style.backgroundColor='#0056b3'; this.style.boxShadow='0 4px 12px rgba(0, 123, 255, 0.4)'"
                          onmouseout="this.style.backgroundColor='#007bff'; this.style.boxShadow='none'"
                          >
                            GO TO WEBSITE
                          </a>
                        </div>
                      </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                      <td style="padding: 20px; text-align: center; background-color: #f0f0f0; font-family: Arial, sans-serif; font-size: 12px; color: #777777;">
                        This is an automated message from Lab Site Generator.<br/>
                        For support, contact the system administrator.
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </body>
        </html>
        """

        message.attach(MIMEText(html_body, 'html'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
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