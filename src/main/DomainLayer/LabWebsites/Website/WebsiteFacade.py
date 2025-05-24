import threading

from src.main.DomainLayer.LabWebsites.Website.ContactInfo import ContactInfo
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.main.DomainLayer.LabWebsites.Website.Website import Website
from src.DAL.DTOs.Website_dto import website_dto
from src.DAL.DAL_controller import DAL_controller
import json

class WebsiteFacade:
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super(WebsiteFacade, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.websites = {} # MAP instead of list
        self.dal_controller = DAL_controller()
        self._load_all_data()

        self._initialized = True

    @classmethod
    def get_instance(cls):
        return cls()

    @classmethod
    def reset_instance(cls):
        """Reset the singleton instance. Useful for unit tests."""
        with cls._instance_lock:
            cls._instance = None

    def add_website(self, website: Website):
        # self.websites.append(website)
        self.websites[website.domain] = website


    def create_new_website(self, domain):
        website = Website(domain)
        self.add_website(website)
        self.dal_controller.website_repo.save(website_dto=website.to_dto()) #===========================================
        return website


    def get_website(self, domain) -> Website:
        # for website in self.websites:
        #     if website.domain == domain:
        #         return website
        # return None
        if domain not in self.websites:
            self._load_website(domain)
        return self.websites.get(domain)


    def get_all_website_domains(self) -> list[str]:
        return self.dal_controller.website_repo.find_all_domains()


    def get_all_approved_publication(self, domain):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        return website.get_all_approved_publication()
    
    def get_all_not_approved_publications(self, domain):
        website = self.get_website(domain=domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        return website.get_all_not_approved_publications()


    def get_all_approved_publications_of_member(self, domain, email):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        return website.get_all_approved_publications_of_member(email)
    
    def get_all_not_approved_publications_of_member(self, domain, email):
        website = self.get_website(domain)
        if website:
            return website.get_all_not_approved_publications_of_member(email)
        else:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)

    #creare new publication manually
    def create_new_publication(self, domain, publication_link, publication_details, git_link, video_link, presentation_link, authors_emails):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        pub_dto =  website.add_publication_manually(publication_link, publication_details, git_link, video_link, presentation_link, authors_emails)
        self.dal_controller.publications_repo.save(publication_dto=pub_dto, domain=domain)
        return pub_dto.get_paper_id()
    
    def create_new_publication_fromDTO(self, domain, pubDTO, author_emails):
        website = self.get_website(domain)
        if not website:
             raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        website.create_publication(publicationDTO=pubDTO, authors_emails=author_emails)
        self.dal_controller.publications_repo.save(publication_dto=pubDTO, domain=domain)
        print(f"publication saved sucessfully")

    def set_publication_video_link(self, domain, publication_id, video_link):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        pub_dto = website.set_publication_video_link(publication_id, video_link)
        self.dal_controller.publications_repo.save(publication_dto=pub_dto, domain=domain)


    def set_publication_git_link(self, domain, publication_id, git_link):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        pub_dto = website.set_publication_git_link(publication_id, git_link)
        self.dal_controller.publications_repo.save(publication_dto=pub_dto, domain=domain)


    def set_publication_presentation_link(self, domain, publication_id, presentation_link):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        pub_dto = website.set_publication_presentation_link(publication_id, presentation_link)
        self.dal_controller.publications_repo.save(publication_dto=pub_dto, domain=domain)


    def error_if_member_is_not_publication_author(self, domain, publication_id, email):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        if not website.check_if_member_is_publication_author(publication_id, email):
            raise Exception(ExceptionsEnum.USER_IS_NOT_PUBLICATION_AUTHOR_OR_LAB_MANAGER)


    def check_if_publication_approved(self, domain, publication_id):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        return website.check_if_publication_approved(publication_id)


    def get_publication_by_paper_id(self, domain, paper_id):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        return website.get_publication_by_paper_id(paper_id)


    def final_approve_publication(self, domain, publication_id):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        pub_dto = website.final_approve_publication(publication_id)
        self.dal_controller.publications_repo.save(publication_dto=pub_dto, domain=domain)


    def set_site_about_us(self, domain, about_us):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        website.set_about_us(about_us)
        self.dal_controller.website_repo.save(website_dto=website.to_dto())


    def set_site_contact_info(self, domain, contact_info_dto):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        website.set_contact_info(contact_info_dto)
        self.dal_controller.website_repo.save(website_dto=website.to_dto())


    def get_about_us(self, domain):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        return website.get_about_us()


    def initial_approve_publication(self, domain, publication_id):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        pub_dto = website.initial_approve_publication(publication_id)
        self.dal_controller.publications_repo.save(publication_dto=pub_dto, domain=domain)


    def reject_publication(self, domain, publication_id):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        pub_dto = website.reject_publication(publication_id)
        self.dal_controller.publications_repo.save(publication_dto=pub_dto, domain=domain)
    

    def get_contact_us(self, domain):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        return website.get_contact_us()
    
    def _load_website(self, domain):
        dto = self.dal_controller.website_repo.find_by_domain(domain=domain)
        if not dto:
            return
        contact_info = None
        if dto.contact_info:
            contact_info_dict = json.loads(dto.contact_info)
            contact_info = ContactInfo(
                lab_mail=contact_info_dict.get("email"),
                lab_phone_num=contact_info_dict.get("phone_num"),
                lab_address=contact_info_dict.get("address")
            )
        website = Website(domain=dto.domain, contact_info=contact_info, about_us=dto.about_us)
        pubs = self.dal_controller.publications_repo.find_by_domain(domain=dto.domain)
        website.load_pub_dtos(pub_list=pubs)
        self.websites[domain] = website
    
    def _load_all_data(self):
        website_dtos = self.dal_controller.website_repo.find_all()
        for dto in website_dtos:
            contact_info = None
            if dto.contact_info:
                contact_info_dict = json.loads(dto.contact_info)
                contact_info = ContactInfo(
                    lab_mail=contact_info_dict.get("email"),
                    lab_phone_num=contact_info_dict.get("phone_num"),
                    lab_address=contact_info_dict.get("address")
                )
            website = Website(domain=dto.domain, contact_info=contact_info, about_us=dto.about_us)
            pubs = self.dal_controller.publications_repo.find_by_domain(domain=dto.domain)
            website.load_pub_dtos(pub_list=pubs)
            self.websites[website.domain] = website
    
    def remove_website_data(self, domain):
        """
        Delete a website.
        """
        #remove website from websites list
        # for website in self.websites:
        #     if website.domain == domain:
        #         self.websites.remove(website)
        #         break
        if domain in self.websites:
            del self.websites[domain]

    def reset_system(self):
        """
        Resets the entire system by clearing all stored websites.
        """
        self.websites.clear()
