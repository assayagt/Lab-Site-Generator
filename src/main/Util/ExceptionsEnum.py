from enum import Enum

class ExceptionsEnum(Enum):
    USER_IS_NOT_MEMBER = "User is not logged in, so he can't perform this operation"
    USER_NOT_EXIST = "User does not exist"
    USER_ALREADY_LOGGED_IN = "user is already logged in"
    USER_NOT_EXIST = "User does not exist"
