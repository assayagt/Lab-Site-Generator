
class website_dto:
    def __init__(self, domain: str, contact_info: str, about_us: str):
        self.domain = domain
        self.contact_info = contact_info
        self.about_us = about_us

    def get_json(self):
        return {
            "domain": self.domain,
            "contact_info": self.contact_info,
            "about_us": self.about_us,
        }

        