from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template

class SiteCustom:
    def __init__(self, domain, name, components, template: Template, logo=None, home_picture=None):
        self.domain = domain
        self.name = name
        self.components = components
        self.template = template
        self.logo = logo
        self.home_picture = home_picture
        self.generated = False

    def change_template(self, template: Template):
        self.template = template

    def add_component(self, components: list):
        if isinstance(components, list):
            self.components.extend(components)  # Adds multiple components at once
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

    def set_generated(self):
        self.generated = True

    def set_logo(self, logo):
        self.logo = logo

    def set_home_picture(self, home_picture):
        self.home_picture = home_picture