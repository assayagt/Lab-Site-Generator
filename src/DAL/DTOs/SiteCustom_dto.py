from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.DomainLayer.LabGenerator.SiteCustom.SiteCustom import SiteCustom

class SiteCustom_dto:
    def __init__(self, domain=None, name=None, components=None, template=None, site_creator_email=None, logo=None, home_picture=None):
        self.domain = domain
        self.name = name
        self.components = components if components is not None else []
        self.template = template
        self.logo = logo
        self.home_picture = home_picture
        self.site_creator_email = site_creator_email

    def to_site_custom(self):
        """Convert a SiteCustomDTO object to a SiteCustom."""
        return SiteCustom(
            domain=self.domain,
            name=self.name,
            components=self.components,
            template=self.template,
            logo=self.logo,
            home_picture=self.home_picture,
            site_creator_email=self.site_creator_email,
        )
    
    def get_json(self):
        return {
            "domain": self.domain,
            "name": self.name,
            "components": self.components,
            "template": self.template,
            "logo": self.logo,
            "home_picture": self.home_picture,
        }