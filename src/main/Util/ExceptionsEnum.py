from enum import Enum

class ExceptionsEnum(Enum):
    USER_IS_NOT_MEMBER = "User is not logged in, so he can't perform this operation"
    USER_NOT_EXIST = "User does not exist"
    USER_ALREADY_LOGGED_IN = "User is already logged in"
    USER_IS_NOT_A_LAB_MEMBER = "User is not a lab member"
    ERROR_SENDING_EMAIL = "Error sending email"
    EMAIL_IS_ALREADY_ASSOCIATED_WITH_A_MEMBER = "The given email is already associated with a member"
    WEBSITE_DOMAIN_NOT_EXIST = "Error! The given domain website does not exist"
    SITE_CREATOR_CANT_BE_ALUMNI = "The site creator cannot be designated as an alumni"
    USER_IS_NOT_A_LAB_MEMBER_OR_LAB_MANAGER = "User is not a lab member or a lab manager"
    USER_IS_NOT_A_LAB_MEMBER_OR_LAB_MANAGER_OR_CREATOR = "User is not a lab member or a lab manager or a site creator"
    USER_IS_NOT_A_LAB_MANAGER = "User is not a lab manager"
    USER_IS_NOT_PUBLICATION_AUTHOR_OR_LAB_MANAGER = "User is not a publication author or a lab manager"
    SITE_INDEX_OUT_OF_RANGE = "Error: Site index out of range"
    INVALID_SITE_NAME = "Error: Invalid site name"
