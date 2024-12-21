from enum import Enum

class ExceptionsEnum(Enum):
    USER_IS_NOT_MEMBER = "User is not logged in, so he can't perform this operation"
    USER_NOT_EXIST = "User does not exist"
    USER_ALREADY_LOGGED_IN = "User is already logged in"
    USER_IS_NOT_A_LAB_MEMBER = "User is not a lab member"
    ERROR_SENDING_EMAIL = "Error sending email"
    EMAIL_IS_ALREADY_ASSOCIATED_WITH_A_MEMBER = "The given email is already associated with a member"
    WEBSITE_DOMAIN_NOT_EXIST = "Error! The given domain website does not exist"
