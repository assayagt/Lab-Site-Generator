from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.DomainLayer.LabGenerator.SiteCustom.SiteCustom import SiteCustom

class SiteCustomDTO:
    def __init__(self, domain=None, name=None, components=None, template=None):
        self.domain = domain
        self.name = name
        self.components = components if components is not None else []
        self.template = template

    @classmethod
    def from_site_custom(cls, site_custom):
        """Convert a SiteCustom object to a SiteCustomDTO."""
        return cls(
            domain=site_custom.domain,
            name=site_custom.name,
            components=site_custom.components,
            template=site_custom.template,
        )

    def to_site_custom(self):
        """Convert a SiteCustomDTO object to a SiteCustom."""
        return SiteCustom(
            domain=self.domain,
            name=self.name,
            components=self.components,
            template=self.template,
        )

    def get_domain(self):
        return self.domain

    def get_name(self):
        return self.name

    def get_components(self):
        return self.components

    def get_template(self):
        return self.template

    def get_json(self):
        return {
            "domain": self.domain,
            "name": self.name,
            "components": self.components,
            "template": self.template,
        }