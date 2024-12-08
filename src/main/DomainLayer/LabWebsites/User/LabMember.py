import State

class LabMember(State):
    def __init__(self, username, secondEmail, linkedin_link, media):
        self.username = username
        self.secondEmail = secondEmail
        self.linkedin_link = linkedin_link
        self.media = media

    def some_operation(self):
        pass