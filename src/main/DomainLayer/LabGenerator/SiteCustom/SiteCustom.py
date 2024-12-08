import Template

class SiteCustom:
    def __init__(self, domain, name, components, template: Template):
        self.domain = domain
        self.name = name
        self.components = components
        self.template = template

    def change_template(self, template: Template):
        self.template = template

    def add_component(self, component):
        self.components.append(component)

    def remove_component(self, component):
        self.components.remove(component)
