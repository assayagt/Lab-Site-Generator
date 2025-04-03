from src.main.DomainLayer.LabGenerator.User import Member


class member_dto:
    def __init__(self, email=None, domain=None):
        self.email = email
        self.domain = domain

    def to_member(self):
        """Convert a MemberDTO object to a Member."""
        # return Member(email = self.email)
        # TODO: implement this method
    
    def get_json(self):
        return {
            "email": self.email,
            "domail": self.domain,
        }