from EmailNotification import EmailNotification
class NotificationsFacade:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NotificationsFacade, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.websocket_handler = None

    def notify_user(self, email_notification):
        email_notification.send_email()

    def send_publication_notification(self, publicationDto, recipientEmail):
        """
        Sends a notification email for a new publication.
        """
        # Format email body
        body = (
            f"New Publication found:\n\n"
            f"Title: {publicationDto.title}\n"
            f"Authors: {', '.join(publicationDto.authors)}\n"
            f"Year: {publicationDto.publication_year}\n"
            f"Link: {publicationDto.publication_link}\n\n"
            f"Please review and approve or reject this publication on your lab site."
        )

        # Create the email notification
        email_notification = EmailNotification(recipientEmail, "New Publication Pending Approval", body)

        self.notify_user(email_notification)

    def send_registration_request_notification(self, requestedEmail, recipientEmail):
        """
        Sends a notification email containing a registration request.
        """
        # Format email body
        body = (
            f"New Registration Request:\n\n"
            f"The user with email address {requestedEmail} has requested to join your lab website.\n\n"
            f"Please log in to your lab site to review and approve or reject this request."
        )

        # Create the email notification
        email_notification = EmailNotification(recipientEmail, "New Registration Request Pending Approval", body)

        self.notify_user(email_notification)
