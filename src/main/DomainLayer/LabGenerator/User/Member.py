import State

class Member(State):
    def __init__(self, user_id=None, member_id=None, username=None):
        self.user_id = user_id
        self.member_id = member_id
        self.username = username

    def logout(self):
        # Do nothing
        pass

    def exit_Generator_system(self):
        pass

    def login(self):
        raise Exception("User is already logged in")

    def get_username(self):
        return self.username

    def get_member_id(self):
        return self.member_id

    def is_member(self):
        return True

    def get_user_id(self):
        return self.user_id

    def set_user_id(self, user_id):
        self.user_id = user_id
