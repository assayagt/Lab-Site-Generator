

class notification_dto:
    def __init__(self, domain=None, id=None, recipient=None, subject=None, body=None, request_email=None, publication_id=None, isRead=None):
        self.domain = domain,
        self.id = id
        self.recipient = recipient
        self.subject = subject
        self.body = body
        self.request_email=request_email
        self.publication_id = publication_id
        self.isRead = isRead

    def get_json(self):
        pass