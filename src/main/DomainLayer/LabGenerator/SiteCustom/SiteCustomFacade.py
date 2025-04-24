import re
import json
import threading

from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.DomainLayer.LabGenerator.SiteCustom.SiteCustom import SiteCustom
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.main.DomainLayer.LabGenerator.SiteCustom.SiteCustomDTO import SiteCustomDTO
from src.DAL.DAL_controller import DAL_controller


class SiteCustomFacade:
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super(SiteCustomFacade, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.sites = {}
        self.dal_controller = DAL_controller()
        self._load_all_siteCustoms()

        self._initialized = True

    @classmethod
    def get_instance(cls):
        return cls()

    @classmethod
    def reset_instance(cls):
        """Reset the singleton instance. Useful for unit tests."""
        with cls._instance_lock:
            cls._instance = None

    def error_if_domain_is_not_valid(self, domain):
        # Regular expression for basic domain validation
        #TODO: probably need to be changed in the future once we know the domains provided by the university
        domain_regex = r'^(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z0-9-]{2,}$'
        if re.match(domain_regex, domain) is None:
            raise Exception(ExceptionsEnum.INVALID_DOMAIN_FORMAT.value)

    def create_new_site(self, domain, name, components, template, email):
        #if not isinstance(template, Template):
        #     raise Exception(ExceptionsEnum.INVALID_TEMPLATE.value)
        if not isinstance(name, str) or not name:
            raise Exception(ExceptionsEnum.INVALID_SITE_NAME.value)
        self.error_if_domain_is_not_valid(domain)
        site = SiteCustom(domain, name, components, template, email)
        self.sites[domain] = site
        self.dal_controller.siteCustom_repo.save(site.to_dto(), email) #===========================================
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
        self.dal_controller.siteCustom_repo.save(siteCustom_dto=site.to_dto()) #===========================================

    def change_site_domain(self, old_domain, new_domain):
        """Changes the domain of a site."""
        if not isinstance(new_domain, str) or not new_domain:
            raise Exception(ExceptionsEnum.INVALID_DOMAIN_FORMAT.value)
        site = self.sites[old_domain]
        self.sites.pop(old_domain, None)
        site.change_domain(new_domain)
        self.sites[new_domain] = site
        self.dal_controller.siteCustom_repo.delete(old_domain)
        self.dal_controller.siteCustom_repo.save(siteCustom_dto=site.to_dto())

    def change_site_template(self, old_domain, new_template):
        """Changes the template of a site."""
        if not isinstance(new_template, Template):
            raise Exception(ExceptionsEnum.INVALID_TEMPLATE.value)
        site = self.sites[old_domain]
        site.change_template(new_template)
        self.dal_controller.siteCustom_repo.save(siteCustom_dto=site.to_dto())

    def add_components_to_site(self, old_domain, components):
        """Adds components to a site."""
        if not isinstance(components, list) or not all(isinstance(c, str) for c in components):
            raise Exception(ExceptionsEnum.INVALID_COMPONENTS_FORMAT.value)
        site = self.sites[old_domain]
        site.add_component(components)
        self.dal_controller.siteCustom_repo.save(siteCustom_dto=site.to_dto())

    def remove_component_from_site(self, old_domain, component):
        """Removes a component from a site."""
        if not isinstance(component, str):
            raise Exception(ExceptionsEnum.INVALID_COMPONENT_FORMAT.value)
        site = self.sites[old_domain]
        site.remove_component(component)
        self.dal_controller.siteCustom_repo.save(siteCustom_dto=site.to_dto())

    def get_custom_websites(self, domains):
        """Get details of custom websites with the given domains. return map of domain, site name, and generated status"""
        custom_sites_details = {}
        for domain in domains:
            site = self.sites[domain]
            custom_sites_details[domain] = {"site_name": site.name, "generated": site.generated}
        return custom_sites_details

    def set_custom_site_as_generated(self, domain):
        """Sets a custom site as generated."""
        site = self.sites[domain]
        site.set_generated()
        self.dal_controller.siteCustom_repo.save(siteCustom_dto=site.to_dto())

    def reset_system(self):
        """
        Resets the entire system by clearing all stored sites.
        """
        self.sites.clear()
        self.dal_controller.drop_all_tables()
       
    def get_site_by_domain(self, domain):
        """Get site by domain, return siteCustomDTO object"""
        site = self.sites[domain]
        site_custom_dto = SiteCustomDTO.from_site_custom(site)
        return site_custom_dto

    def set_logo(self, domain, logo):
        """Set logo to site"""
        site = self.sites[domain]
        site.set_logo(logo)
        self.dal_controller.siteCustom_repo.save(siteCustom_dto=site.to_dto())

    def set_home_picture(self, domain, home_picture):
        """Set home picture to site"""
        site = self.sites[domain]
        site.set_home_picture(home_picture)
        self.dal_controller.siteCustom_repo.save(siteCustom_dto=site.to_dto())

    def error_if_user_is_not_site_creator(self, email, domain):
        site = self.sites[domain]
        if site.get_site_creator_email() != email:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_SITE_CREATOR.value)

    def get_site_creator_email(self, domain):
        site = self.sites[domain]
        return site.get_site_creator_email()

    def set_site_creator(self, domain, nominated_email):
        site = self.sites[domain]
        site.set_site_creator_email(nominated_email)
        self.dal_controller.siteCustom_repo.delete(domain=site.domain)
        self.dal_controller.siteCustom_repo.save(siteCustom_dto=site.to_dto())

    def _load_all_siteCustoms(self):
        res = self.dal_controller.siteCustom_repo.find_all()
        print(res)
        for dto in res:
            if dto.template is not None:
                template = Template(dto.template)
            else:
                template = None
            self.sites[dto.domain] = SiteCustom(
                domain=dto.domain,
                name=dto.name,
                components=json.loads(dto.components_str),
                template=template,
                site_creator_email=dto.site_creator_email,
                logo=dto.logo,
                home_picture=dto.home_picture,
                generated=bool(dto.generated)
            )