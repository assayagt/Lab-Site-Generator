from State import State
from src.main.Util.ExceptionsEnum import ExceptionsEnum

class Guest(State):
    def __init__(self):
        super().__init__()

    def get_member_id(self):
        return None

    def logout(self):
        raise Exception(ExceptionsEnum.USER_IS_NOT_MEMBER.value)

    def login(self):
        # Do nothing
        return

    def is_member(self):
        return False

    def get_username(self):
        return None