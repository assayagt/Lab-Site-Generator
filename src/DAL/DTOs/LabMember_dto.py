

class lab_member_dto:
    def __init__(self,domain=None, email=None, second_email=None, linkedin_link=None, media=None, full_name=None, degree=None, bio=None):
        self.domain=domain
        self.email = email
        self.second_email=second_email
        self.linkedin_link=linkedin_link
        self.media=media
        self.full_name=full_name
        self.degree=degree.value
        self.bio=bio

    