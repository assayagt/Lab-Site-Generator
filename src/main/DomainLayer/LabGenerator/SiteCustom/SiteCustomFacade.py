import Template,SiteCustom

class SiteCustomFacade:
    _singleton_instance = None

    def __init__(self):
        if SiteCustomFacade._singleton_instance is not None:
            raise Exception("This is a singleton class!")
        self.sites = []

    @staticmethod
    def get_instance():
        if SiteCustomFacade._singleton_instance is None:
            SiteCustomFacade._singleton_instance = SiteCustomFacade()
        return SiteCustomFacade._singleton_instance

    def create_new_site(self, domain, name, components, template: Template):
        site = SiteCustom(domain, name, components, template)
        self.sites.append(site)
