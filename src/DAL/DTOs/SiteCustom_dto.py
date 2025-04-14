# from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
# from src.main.DomainLayer.LabGenerator.SiteCustom.SiteCustom import SiteCustom
import json

class siteCustom_dto:
    def __init__(self, domain=None, name=None, components_str:str=None, components_list:list=None, template=None, site_creator_email=None,
                  logo=None, home_picture=None, generated=False):
        self.domain = domain
        self.name = name
        if components_str is None:
            self.components_str = json.dumps(components_list) if components_list is not None else json.dumps([])
        else:
            self.components_str = components_str
        self.template = template.value
        self.logo = logo
        self.home_picture = home_picture
        self.site_creator_email = site_creator_email
        self.generated = generated

    # def to_site_custom(self):
    #     """Convert a SiteCustomDTO object to a SiteCustom."""
    #     return SiteCustom(
    #         domain=self.domain,
    #         name=self.name,
    #         components=json.loads(self.components_str),
    #         template=self.template,
    #         logo=self.logo,
    #         home_picture=self.home_picture,
    #         site_creator_email=self.site_creator_email
    #     )
    
    def get_json(self):
        return {
            "domain": self.domain,
            "name": self.name,
            "components": json.loads(self.components_str),
            "template": self.template,
            "logo": self.logo,
            "home_picture": self.home_picture,
        }