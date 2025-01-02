from src.main.DomainLayer.LabGenerator.User.State import State
from src.main.DomainLayer.LabGenerator.User.Guest import Guest

class User:
    def __init__(self, user_id=None):
        self.user_id = user_id
        self.state = Guest()
        self.is_guest = not self.state.is_member()

    def set_state(self, state: State):
        self.state = state
        self.is_guest = not state.is_member()

    def logout(self):
        self.state.logout()
        self.state = Guest()
        self.is_guest = not self.state.is_member()

    def login(self, login_member):
        self.state.login()
        self.set_state(login_member)
        self.is_guest = not self.state.is_member()

    def get_user_id(self):
        return self.user_id

    def get_email(self):
        return self.state.get_email()

    def is_member(self):
        pass