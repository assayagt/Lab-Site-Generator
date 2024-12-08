import State, Guest

class User:
    def __init__(self, state: State, user_id=None):
        self.state = state
        self.user_id = user_id
        self.is_guest = not state.is_member()
        self.member_id = None
        self.state: State = Guest()

    def set_state(self, state: State):
        self.state = state
        self.is_guest = not state.is_member()
        self.member_id = state.get_member_id()

    def logout(self):
        self.state.logout()
        self.state = Guest()
        self.is_guest = not self.state.is_member()
        self.member_id = None

    def login(self, login_member):
        self.state.logout()
        self.set_state(login_member)


