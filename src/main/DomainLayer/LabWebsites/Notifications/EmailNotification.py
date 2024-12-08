class EmailNotification:
    def __init__(self, recipient, subject, body):
        self.recipient = recipient
        self.subject = subject
        self.body = body

    def send_email(self):
        print(f"Sending email to {self.recipient}")
        print(f"Subject: {self.subject}")
        print(f"Body: {self.body}")
