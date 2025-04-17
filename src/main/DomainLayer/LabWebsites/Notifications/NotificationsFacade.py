import uuid

from src.main.DomainLayer.LabWebsites.Notifications.WebSocketHandler import WebSocketHandler
from src.main.DomainLayer.LabWebsites.Notifications.EmailNotification import EmailNotification
from src.DAL.DAL_controller import DAL_controller


class NotificationsFacade:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NotificationsFacade, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.websocket_handler = None
        self.email_notifications_center = {}  # { website_id: { user_email: [notification_list] } }
        self.dal_controller = DAL_controller()
        self.web_socket_handler = WebSocketHandler()

    def notify_user(self, email_notification, domain, recipientEmail):
        if domain not in self.email_notifications_center:
            self.email_notifications_center[domain] = {}

        if recipientEmail not in self.email_notifications_center[domain]:
            self.email_notifications_center[domain][recipientEmail] = []

        self.email_notifications_center[domain][recipientEmail].append(email_notification)
        self.dal_controller.notifications_repo.save_notification(email_notification.to_dto())  # Save the notification to the database

        email_notification.send_email()

        # Send live notification
        event = ""
        match email_notification.subject:
            case "New Publication Pending Approval":
                event = "initial-publication-notification"

            case "New Publication Pending Final Approval":
                event = "final-publication-notification"

            case "New Registration Request Pending Approval":
                event = "registration-notification"

        self.web_socket_handler.emit_to_user(
            domain,
            recipientEmail,
            event,
            {
                'id': email_notification.id,  # unique ID for the publication
                'body': email_notification.body,
                'subject': email_notification.subject
            }
        )

    def send_publication_notification(self, publicationDto, recipientEmail, domain):
        """
        Sends a notification email for a new publication to its authors.
        """
        # Format email body
        body = (
            f"New Publication found:\n\n"
            f"Title: {publicationDto.title}\n"
            f"Authors: {', '.join(publicationDto.authors)}\n"
            f"Year: {publicationDto.publication_year}\n"
            f"Link: {publicationDto.publication_link}\n\n"
            f"Please review and approve or reject this publication."
        )

        # Create the email notification
        id = str(uuid.uuid4())

        email_notification = EmailNotification(id, recipientEmail, "New Publication Pending Approval", body, domain, publication_id=publicationDto.get_paper_id())

        # Send Email notification and save it
        self.notify_user(email_notification, domain, recipientEmail)

    def send_publication_notification_for_final_approval(self, publicationDto, recipientEmail, domain):
        """
        Sends a notification email for final approval of a publication to the lab mangers
        """
        # Format email body
        body = (
            f"Publication Initially Approved By Author:\n\n"
            f"Title: {publicationDto.title}\n"
            f"Authors: {', '.join(publicationDto.authors)}\n"
            f"Year: {publicationDto.publication_year}\n"
            f"Link: {publicationDto.publication_link}\n\n"
            f"This publication has been initially approved by it's author, please review and give final approval on your lab site."
        )

        # Create the email notification
        id = str(uuid.uuid4())

        email_notification = EmailNotification(id, recipientEmail, "New Publication Pending Final Approval", body, domain, publication_id=publicationDto.get_paper_id())

        # Send Email notification and save it
        self.notify_user(email_notification, domain, recipientEmail)

    def send_registration_request_notification(self, requestedEmail, recipientEmail, domain):
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

        # Create ssuid
        id = str(uuid.uuid4())
        email_notification = EmailNotification(id, recipientEmail, "New Registration Request Pending Approval", body, domain, request_email=requestedEmail)

        #Send Email notification and save it
        self.notify_user(email_notification, domain, recipientEmail)


    def get_notifications_for_user(self, domain, user_email, unread_only=True):
        """
        Retrieves notifications for a user in a specific website domain.
        Returns a list of dictionaries with notification details.
        """
        if domain not in self.email_notifications_center or user_email not in self.email_notifications_center[domain]:
            return []

        notifications = self.email_notifications_center[domain][user_email]

        return [
            n.to_dict() for n in notifications if not unread_only or not n.get_is_read()
        ]

    def mark_notification_as_read(self, domain, user_email, notification_id):
        """
        Marks a specific notification as read using its ID.
        Returns the request_email or publication_id based on which one is set.
        """
        if domain in self.email_notifications_center and user_email in self.email_notifications_center[domain]:
            notifications = self.email_notifications_center[domain][user_email]

            for n in notifications:
                if n.id == notification_id:
                    n.mark_as_read()
                    self.dal_controller.notifications_repo.save_notification(n.to_dict())
                    return n.request_email or n.publication_id

    def connect_user_socket(self, email, domain, sid):
        """
        Connects a user to the WebSocket server.
        """
        self.web_socket_handler.register_user(email, domain, sid)

    def disconnect_user_socket(self, sid):
        """
        Disconnects a user from the WebSocket server.
        """
        self.web_socket_handler.unregister_user_by_sid(sid)