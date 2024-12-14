import Member

class UserFacade:
    _singleton_instance = None

    def __init__(self):
        if UserFacade._singleton_instance is not None:
            raise Exception("This is a singleton class!")
        self.users = {}
        self.members_sites = {}

    @staticmethod
    def get_instance():
        if UserFacade._singleton_instance is None:
            UserFacade._singleton_instance = UserFacade()
        return UserFacade._singleton_instance

    def create_new_site_manager(self, email, domain):
        if domain not in self.members_sites[email]["domains"]:
            self.members_sites[email]["domains"].append(domain)

    def login(self, userId, email):
        """Handle login logic after retrieving user info."""
        user = self.get_user_by_id(userId)
        member = self.get_member_by_email(email)
        if member is not None:
            member.setUserId(userId)
        else:
            member = Member(user_id=userId, email=email)
            self.members_sites[email] = {"member": member, "domains": []}
        user.login(member)

    def logout(self, userId):
        user = self.get_user_by_id(userId)
        user.logout()

    def get_member_by_email(self, email):
        """Retrieve a Member object by email."""
        if email in self.members_sites:
            return self.members_sites[email]["member"]
        return None

    def get_user_by_id(self, userId):
        if userId in self.users:
            user = self.users[userId]
        else:
            user = None
        return user

    def error_if_user_notExist(self, userId):
        if self.get_user_by_id(userId) is None:
            raise Exception("User not exist!")
