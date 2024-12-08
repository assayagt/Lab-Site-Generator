import EmailNotification
class NotificationsFacade:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NotificationsFacade, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.websocket_handler = None

    def notify_user(self, email_notification: EmailNotification):
        email_notification.send_email()