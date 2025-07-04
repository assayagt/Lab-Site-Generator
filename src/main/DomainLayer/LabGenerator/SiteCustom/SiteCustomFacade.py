import base64
import os
import re
import json
import threading

from src.main.DomainLayer.LabGenerator.SiteCustom.Template import Template
from src.main.DomainLayer.LabGenerator.SiteCustom.SiteCustom import SiteCustom
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.DAL.DTOs.SiteCustom_dto import siteCustom_dto
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
        self._initialized = True

    @classmethod
    def get_instance(cls):
        return cls()

    @classmethod
    def reset_instance(cls):
        """Reset the singleton instance. Useful for unit tests."""
        with cls._instance_lock:
            cls._instance = None

    def get_site_by_domain(self, domain) -> SiteCustom:
        self.error_if_domain_not_exist(domain)
        """Retrieves the site custom from the database"""
        dto = self.dal_controller.siteCustom_repo.find_by_domain(domain)
        return self._site_custom_dto_to_site_custom(dto)

    def error_if_domain_is_not_valid(self, domain):
        # Regular expression for basic domain validation
        # TODO: probably need to be changed in the future once we know the domains provided by the university
        domain_regex = (
            r"^(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z0-9-]{2,}$"
        )
        if re.match(domain_regex, domain) is None:
            raise Exception(ExceptionsEnum.INVALID_DOMAIN_FORMAT.value)

    def create_new_site(self, domain, name, components, template, email):
        # if not isinstance(template, Template):
        #     raise Exception(ExceptionsEnum.INVALID_TEMPLATE.value)
        if not isinstance(name, str) or not name:
            raise Exception(ExceptionsEnum.INVALID_SITE_NAME.value)
        self.error_if_domain_is_not_valid(domain)
        site = SiteCustom(domain, name, components, template, email)
        if "Media" in components:
            gallery_path = self.create_gallery_directory(domain)
            site.set_gallery_path(gallery_path)
        self.dal_controller.siteCustom_repo.save(site.to_dto(), email)
        return site

    def error_if_domain_already_exist(self, domain):
        custom = self.dal_controller.siteCustom_repo.find_by_domain(domain)
        if custom:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_ALREADY_EXIST.value)

    def error_if_domain_not_exist(self, domain):
        custom = self.dal_controller.siteCustom_repo.find_by_domain(domain)
        if not custom:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST.value)

    def change_site_name(self, domain, new_name):
        """Changes the name of a site."""
        if not isinstance(new_name, str) or not new_name:
            raise Exception(ExceptionsEnum.INVALID_SITE_NAME.value)
        site: SiteCustom = self.get_site_by_domain(domain)
        site.change_name(new_name)
        self.dal_controller.siteCustom_repo.save(siteCustom_dto=site.to_dto())

    def change_site_domain(self, old_domain, new_domain):
        """Changes the domain of a site."""
        if not isinstance(new_domain, str) or not new_domain:
            raise Exception(ExceptionsEnum.INVALID_DOMAIN_FORMAT.value)
        site: SiteCustom = self.get_site_by_domain(old_domain)
        site.change_domain(new_domain)
        self.dal_controller.siteCustom_repo.delete(old_domain)
        self.dal_controller.siteCustom_repo.save(siteCustom_dto=site.to_dto())

    def change_site_template(self, domain, new_template):
        """Changes the template of a site."""
        if not isinstance(new_template, Template):
            raise Exception(ExceptionsEnum.INVALID_TEMPLATE.value)
        site = self.get_site_by_domain(domain=domain)
        site.change_template(new_template)
        self.dal_controller.siteCustom_repo.save(siteCustom_dto=site.to_dto())

    def add_components_to_site(self, domain, components):
        """Adds components to a site."""
        if not isinstance(components, list) or not all(
            isinstance(c, str) for c in components
        ):
            raise Exception(ExceptionsEnum.INVALID_COMPONENTS_FORMAT.value)
        site = self.get_site_by_domain(domain)
        site.add_component(components)
        if "Media" in components:
            gallery_path = self.create_gallery_directory(domain)
            site.set_gallery_path(gallery_path)
        self.dal_controller.siteCustom_repo.save(siteCustom_dto=site.to_dto())

    def remove_component_from_site(self, domain, component):
        """Removes a component from a site."""
        if not isinstance(component, str):
            raise Exception(ExceptionsEnum.INVALID_COMPONENT_FORMAT.value)
        site = self.get_site_by_domain(domain)
        site.remove_component(component)
        self.dal_controller.siteCustom_repo.save(siteCustom_dto=site.to_dto())

    def get_custom_websites(self, domains):
        """Get details of custom websites with the given domains. return map of domain, site name, and generated status"""
        custom_sites_details = {}
        for domain in domains:
            site = self.get_site_by_domain(domain)
            custom_sites_details[domain] = {
                "site_name": site.name,
                "generated": site.generated,
            }
        return custom_sites_details

    def set_custom_site_as_generated(self, domain):
        """Sets a custom site as generated."""
        site = self.get_site_by_domain(domain)
        site.set_generated()
        self.dal_controller.siteCustom_repo.save(siteCustom_dto=site.to_dto())

    def set_logo(self, domain, logo):
        """Set logo to site"""
        site = self.get_site_by_domain(domain)
        site.set_logo(logo)
        self.dal_controller.siteCustom_repo.save(siteCustom_dto=site.to_dto())

    def set_home_picture(self, domain, home_picture):
        """Set home picture to site"""
        site = self.get_site_by_domain(domain)
        site.set_home_picture(home_picture)
        self.dal_controller.siteCustom_repo.save(siteCustom_dto=site.to_dto())

    def error_if_user_is_not_site_creator(self, email, domain):
        site = self.get_site_by_domain(domain)
        if site.get_site_creator_email() != email:
            raise Exception(ExceptionsEnum.USER_IS_NOT_A_SITE_CREATOR.value)

    def get_site_creator_email(self, domain):
        site = self.get_site_by_domain(domain)
        return site.get_site_creator_email()

    def set_site_creator(self, domain, nominated_email):
        site = self.get_site_by_domain(domain)
        site.set_site_creator_email(nominated_email)
        # self.dal_controller.siteCustom_repo.delete(domain=site.domain)
        self.dal_controller.siteCustom_repo.save(siteCustom_dto=site.to_dto())

    def get_if_site_is_generated(self, domain):
        site = self.get_site_by_domain(domain)
        return site.generated

    def delete_website(self, domain):
        """
        Delete a website.
        """
        self.dal_controller.siteCustom_repo.delete(domain)

    def reset_system(self):
        """
        Resets the entire system by clearing all stored sites.
        """
        self.dal_controller.drop_all_tables()

    def create_gallery_directory(self, domain):
        """
        Create a gallery directory for the site.
        """
        website_folder = os.path.join("LabWebsitesUploads", domain)
        gallery_folder = os.path.join(website_folder, "gallery")
        os.makedirs(gallery_folder, exist_ok=True)
        return gallery_folder

    def get_gallery_images(self, domain):
        gallery_images = []
        self.error_if_domain_not_exist(domain)
        site = self.get_site_by_domain(domain)
        gallery_path = site.get_gallery_path()
        if gallery_path and os.path.exists(gallery_path):
            # Get all files in the gallery directory
            for filename in os.listdir(gallery_path):
                file_path = os.path.join(gallery_path, filename)
                # Check if it's a file and has a valid image extension
                if os.path.isfile(file_path):
                    extension = os.path.splitext(filename)[1].lower()
                    if extension in [".jpg", ".jpeg", ".png", ".gif"]:
                        try:
                            with open(file_path, "rb") as image_file:
                                # Determine the correct MIME type
                                if extension == ".jpg" or extension == ".jpeg":
                                    mime_type = "image/jpeg"
                                elif extension == ".png":
                                    mime_type = "image/png"
                                elif extension == ".gif":
                                    mime_type = "image/gif"
                                else:
                                    mime_type = "application/octet-stream"

                                # Encode the image
                                image_base64 = base64.b64encode(
                                    image_file.read()
                                ).decode()
                                image_data_url = (
                                    f"data:{mime_type};base64,{image_base64}"
                                )
                                gallery_images.append(
                                    {"filename": filename, "data_url": image_data_url}
                                )
                        except Exception as e:
                            print(f"Error processing image {filename}: {str(e)}")
                            continue
        return gallery_images

    def delete_gallery_image(self, domain, image_filename):
        """
        Delete an image from the gallery.
        """
        site = self.get_site_by_domain(domain)
        gallery_path = site.get_gallery_path()
        if gallery_path:
            image_path = os.path.join(gallery_path, image_filename)
            if os.path.exists(image_path):
                os.remove(image_path)
            else:
                raise Exception(ExceptionsEnum.IMAGE_NOT_FOUND.value)
        else:
            raise Exception(ExceptionsEnum.GALLERY_NOT_FOUND.value)

    def _site_custom_dto_to_site_custom(self, dto: siteCustom_dto) -> SiteCustom:
        template = Template(dto.template) if dto.template else None
        return SiteCustom(
            domain=dto.domain,
            name=dto.name,
            components=json.loads(dto.components_str),
            template=template,
            site_creator_email=dto.site_creator_email,
            logo=dto.logo,
            home_picture=dto.home_picture,
            generated=bool(dto.generated),
            gallery_path=dto.gallery_path,
        )
