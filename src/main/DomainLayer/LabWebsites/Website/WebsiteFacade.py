from src.main.Util.ExceptionsEnum import ExceptionsEnum
from Website import Website
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
    def create_new_publication(self, domain, publicationDTO, authors_emails):
        website = self.get_website(domain)
        if website is None:
            raise Exception(ExceptionsEnum.WEBSITE_DOMAIN_NOT_EXIST)
        website.create_publication(publicationDTO, authors_emails)
