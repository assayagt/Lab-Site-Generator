import State

class Guest(State):
    def __init__(self):
        super().__init__()

    def get_member_id(self):
        return None

    def logout(self):
        raise ValueError("Only a member can log out")

    def exit_Generator_system(self):
        pass

    def login(self):
        # Do nothing
        return

    def is_member(self):
        return False

    def get_username(self):
        return None