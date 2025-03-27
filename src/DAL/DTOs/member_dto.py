from src.main.DomainLayer.LabGenerator.User import Member


class member_dto:
    def __init__(self, user_id=None, email=None):
        self.user_id = user_id
        self.email = email

    def to_member(self):
        """Convert a SiteCustomDTO object to a SiteCustom."""
        return Member(
            user_id=self.user_id,
            email = self.email
        )
    
    def get_json(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
        }