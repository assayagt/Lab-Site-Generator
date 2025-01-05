import re

from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.DomainLayer.LabGenerator.SiteCustom.SiteCustom import SiteCustom
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.main.DomainLayer.LabGenerator.SiteCustom.SiteCustomDTO import SiteCustomDTO


class SiteCustomFacade:
    _singleton_instance = None

    def __init__(self):
        if SiteCustomFacade._singleton_instance is not None:
            raise Exception("This is a singleton class!")
        self.sites = {}

    @staticmethod
    def get_instance():
        if SiteCustomFacade._singleton_instance is None:
            SiteCustomFacade._singleton_instance = SiteCustomFacade()
        return SiteCustomFacade._singleton_instance

    def error_if_domain_is_not_valid(self, domain):
        # Regular expression for basic domain validation
        #TODO: probably need to be changed in the future once we know the domains provided by the university
        domain_regex = r'^(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z0-9-]{2,}$'
        if re.match(domain_regex, domain) is None:
            raise Exception(ExceptionsEnum.INVALID_DOMAIN_FORMAT.value)

    def create_new_site(self, domain, name, components, template):
        # if not isinstance(template, Template):
        #     raise Exception(ExceptionsEnum.INVALID_TEMPLATE.value)
        if not isinstance(name, str) or not name:
            raise Exception(ExceptionsEnum.INVALID_SITE_NAME.value)
        self.error_if_domain_is_not_valid(domain)
        site = SiteCustom(domain, name, components, template)
        self.sites[domain] = site
        return site

    def error_if_domain_already_exist(self, domain):
        if domain in self.sites:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_ALREADY_EXIST.value)

    def error_if_domain_not_exist(self, domain):
        if domain not in self.sites:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST.value)


    def change_site_name(self, domain, new_name):
        """Changes the name of a site."""
        if not isinstance(new_name, str) or not new_name:
            raise Exception(ExceptionsEnum.INVALID_SITE_NAME.value)
        site = self.sites[domain]
        site.change_name(new_name)

    def change_site_domain(self, old_domain, new_domain):
        """Changes the domain of a site."""
        if not isinstance(new_domain, str) or not new_domain:
            raise Exception(ExceptionsEnum.INVALID_DOMAIN_FORMAT.value)
        site = self.sites[old_domain]
        site.change_domain(new_domain)

    def change_site_template(self, old_domain, new_template):
        """Changes the template of a site."""
        if not isinstance(new_template, Template):
            raise Exception(ExceptionsEnum.INVALID_TEMPLATE.value)
        site = self.sites[old_domain]
        site.change_template(new_template)

    def add_components_to_site(self, old_domain, components):
        """Adds components to a site."""
        if not isinstance(components, list) or not all(isinstance(c, str) for c in components):
            raise Exception(ExceptionsEnum.INVALID_COMPONENTS_FORMAT.value)
        site = self.sites[old_domain]
        site.add_component(components)

    def remove_component_from_site(self, old_domain, component):
        """Removes a component from a site."""
        if not isinstance(component, str):
            raise Exception(ExceptionsEnum.INVALID_COMPONENT_FORMAT.value)
        site = self.sites[old_domain]
        site.remove_component(component)

    def get_custom_websites(self):
        """Get all lab websites. return map of domain and site name"""

        return {site.domain: site.name for site in self.sites}

    def set_custom_site_as_generated(self, domain):
        """Sets a custom site as generated."""
        site = self.sites[domain]
        site.set_generated()

    def reset_system(self):
        """
        Resets the entire system by clearing all stored sites.
        """
        self.sites.clear()
       
    def get_site_by_domain(self, domain):
        """Get site by domain."""
        try:
            #return siteCustomDTO object
            site = self.sites[domain]
            site_custom_dto = SiteCustomDTO.from_site_custom(site)
            return site_custom_dto
        except IndexError:
            raise Exception("Error: Site index out of range")
        except Exception as e:
            raise Exception(f"Unexpected error: {e}")

