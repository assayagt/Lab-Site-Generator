from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.DAL.DTOs.SiteCustom_dto import siteCustom_dto


class SiteCustom:
    def __init__(
        self,
        domain,
        name,
        components,
        template: Template,
        site_creator_email,
        logo=None,
        home_picture=None,
        generated=False,
        gallery_path=None,
    ):
        self.domain = domain
        self.name = name
        self.components = components
        self.template = template
        self.logo = logo
        self.home_picture = home_picture
        self.generated = generated
        self.site_creator_email = site_creator_email
        self.gallery_path = gallery_path

    def change_template(self, template: Template):
        self.template = template

    def add_component(self, components: list):
        if isinstance(components, list):
            self.components = components  # Adds multiple components at once
        else:
            raise TypeError("The input should be a list of components")

    def remove_component(self, component):
        if component in self.components:
            self.components.remove(component)

    def change_name(self, new_name: str):
        self.name = new_name

    def change_domain(self, new_domain: str):
        self.domain = new_domain

    def get_domain(self):
        return self.domain

    def get_name(self):
        return self.name

    def set_generated(self):
        self.generated = True

    def set_logo(self, logo):
        self.logo = logo

    def get_logo(self):
        return self.logo

    def set_home_picture(self, home_picture):
        self.home_picture = home_picture

    def get_home_picture(self):
        return self.home_picture

    def get_site_creator_email(self):
        return self.site_creator_email

    def get_components(self):
        return self.components

    def get_template(self):
        return self.template

    def set_site_creator_email(self, site_creator_email):
        self.site_creator_email = site_creator_email

    def set_gallery_path(self, gallery_path):
        self.gallery_path = gallery_path

    def get_gallery_path(self):
        return self.gallery_path

    def to_dto(self):
        return siteCustom_dto(
            domain=self.domain,
            name=self.name,
            components_list=self.components,
            template=self.template.value if self.template else None,
            logo=self.logo,
            home_picture=self.home_picture,
            site_creator_email=self.site_creator_email,
            generated=self.generated,
            gallery_path=self.gallery_path if self.gallery_path else None,
        )
