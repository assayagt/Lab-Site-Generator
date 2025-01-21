from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.main.DomainLayer.LabWebsites.Website.Website import Website
class WebsiteFacade:
    def __init__(self):
        self.websites = []

    def add_website(self, website):
        self.websites.append(website)

    def create_new_website(self, domain):
        website = Website(domain)
        self.add_website(website)

    def get_website(self, domain):
        for website in self.websites:
            if website.domain == domain:
                return website
        return None

    def get_all_websites(self):
        return self.websites

    def get_all_approved_publication(self, domain):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        return website.get_all_approved_publication()

    def get_all_approved_publications_of_member(self, domain, email):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        return website.get_all_approved_publications_of_member(email)

    #creare new publication manually
    def create_new_publication(self, domain, publication_link, publication_details, git_link, video_link, presentation_link):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        return website.add_publication_manually(publication_link, publication_details, git_link, video_link, presentation_link)

    def set_publication_video_link(self, domain, publication_id, video_link):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        website.set_publication_video_link(publication_id, video_link)

    def set_publication_git_link(self, domain, publication_id, git_link):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        website.set_publication_git_link(publication_id, git_link)

    def set_publication_presentation_link(self, domain, publication_id, presentation_link):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        website.set_publication_presentation_link(publication_id, presentation_link)

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
        website.final_approve_publication(publication_id)

    def set_site_about_us(self, domain, about_us):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        website.set_about_us(about_us)

    def set_site_contact_info(self, domain, contact_info_dto):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        website.set_contact_info(contact_info_dto)

    def get_about_us(self, domain):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        return website.get_about_us()

    def initial_approve_publication(self, domain, publication_id):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        website.initial_approve_publication(publication_id)

    def reject_publication(self, domain, publication_id):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        website.reject_publication(publication_id)
