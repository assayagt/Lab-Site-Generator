from src.main.DomainLayer.LabWebsites.Website.ApprovalStatus import ApprovalStatus
from src.main.DomainLayer.LabWebsites.Website.PublicationDTO import PublicationDTO
from src.DAL.DTOs.Website_dto import website_dto
from src.DAL.DTOs.NewsRecord_dto import NewsRecord_dto
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.DAL.DAL_controller import DAL_controller
import json

class Website:
    def __init__(self, domain, contact_info=None, about_us=None):
        self.domain = domain
        self.contact_info = contact_info
        self.about_us = about_us
        self.dal_controller = DAL_controller()

    def create_publication(self, publicationDTO, authors_emails):
        # Check if publication already exists
        existing_pub = self.dal_controller.publications_repo.find_by_id(publicationDTO.get_paper_id())
        if existing_pub:
            if existing_pub.approved == ApprovalStatus.APPROVED:
                raise Exception(ExceptionsEnum.PUBLICATION_ALREADY_APPROVED.value)
            else:
                raise Exception(ExceptionsEnum.PUBLICATION_ALREADY_WAITING.value)
        
        # Save the publication
        self.dal_controller.publications_repo.save(publication_dto=publicationDTO, domain=self.domain)
        print("publication added to website successfully")

    def update_publication(self, publicationDTO: PublicationDTO):
        # Update the publication in the database
        self.dal_controller.publications_repo.save(publication_dto=publicationDTO, domain=self.domain)

    def add_publication_manually(self, publication_link, publication_details, git_link, video_link, presentation_link,
                                 authors_emails) -> PublicationDTO:
        # publication_dto = PublicationDTO(publication_details["title"],
        #                         publication_details["authors"],
        #                         publication_details["publication_year"],
        #                         ApprovalStatus.FINAL_PENDING.value,
        #                                  publication_link, git_link, video_link, presentation_link,
        #                                  publication_details["description"])
        publication_dto = PublicationDTO(
            title=publication_details["title"],
            publication_year=publication_details["publication_year"],
            publication_link=publication_link,
            approved=ApprovalStatus.FINAL_PENDING,
            git_link=git_link,
            authors=publication_details["authors"],
            video_link=video_link,
            presentation_link=presentation_link,
            description=publication_details["description"],
            author_emails=authors_emails,
            domain=self.domain
        )
        self.create_publication(publication_dto, authors_emails)
        return publication_dto

    def check_publication_exist(self, publication):
        return self.dal_controller.publications_repo.find_by_id(publication.get_paper_id()) is not None

    def get_all_approved_publication(self):
        publications = self.dal_controller.publications_repo.find_by_domain(self.domain)
        return [pub.to_dict() for pub in publications if pub.approved == ApprovalStatus.APPROVED]
    
    def get_all_not_approved_publications(self):
        publications = self.dal_controller.publications_repo.find_by_domain(self.domain)
        return [pub for pub in publications if pub.approved != ApprovalStatus.APPROVED.value]

    def check_if_publication_approved(self, publication_paper_id):
        publication = self.dal_controller.publications_repo.find_by_id(publication_paper_id)
        return publication is not None and publication.approved == ApprovalStatus.APPROVED

    def get_all_approved_publications_of_member(self, email):
        publications = self.dal_controller.publications_repo.find_by_domain(self.domain)
        return [pub.to_dict() for pub in publications if pub.approved == ApprovalStatus.APPROVED and email in pub.author_emails]
    
    def get_all_not_approved_publications_of_member(self, email):
        publications = self.dal_controller.publications_repo.find_by_domain(self.domain)
        return [pub.to_dict() for pub in publications if pub.approved != ApprovalStatus.APPROVED.value and email in pub.author_emails]

    def set_publication_video_link(self, publication_paper_id, video_link) -> PublicationDTO:
        publication = self.dal_controller.publications_repo.find_by_id(publication_paper_id)
        if publication:
            publication.set_video_link(video_link)
            self.dal_controller.publications_repo.save(publication_dto=publication, domain=self.domain)
            return publication
        raise Exception(ExceptionsEnum.PUBLICATION_NOT_FOUND.value)

    def set_publication_git_link(self, publication_paper_id, git_link) -> PublicationDTO:
        publication = self.dal_controller.publications_repo.find_by_id(publication_paper_id)
        if publication:
            publication.set_git_link(git_link)
            self.dal_controller.publications_repo.save(publication_dto=publication, domain=self.domain)
            return publication
        raise Exception(ExceptionsEnum.PUBLICATION_NOT_FOUND.value)

    def set_publication_presentation_link(self, publication_paper_id, link) -> PublicationDTO:
        publication = self.dal_controller.publications_repo.find_by_id(publication_paper_id)
        if publication:
            publication.set_presentation_link(link)
            self.dal_controller.publications_repo.save(publication_dto=publication, domain=self.domain)
            return publication
        raise Exception(ExceptionsEnum.PUBLICATION_NOT_FOUND.value)

    def check_if_member_is_publication_author(self, publication_paper_id, email):
        publication = self.dal_controller.publications_repo.find_by_id(publication_paper_id)
        return publication is not None and email in publication.author_emails

    def get_publication_by_paper_id(self, paper_id) -> PublicationDTO:
        publication = self.dal_controller.publications_repo.find_by_id(paper_id)
        if not publication:
            raise Exception(ExceptionsEnum.PUBLICATION_NOT_FOUND.value)
        return publication
    
    def is_publication_rejected(self, paper_id):
        publication = self.get_publication_by_paper_id(paper_id)
        return publication.approved == ApprovalStatus.REJECTED

    def final_approve_publication(self, paper_id) -> PublicationDTO:
        publication = self.get_publication_by_paper_id(paper_id)
        publication.approved = ApprovalStatus.APPROVED
        self.dal_controller.publications_repo.save(publication_dto=publication, domain=self.domain)
        return publication

    def get_domain(self):
        return self.domain

    def get_about_us(self):
        return self.about_us

    def set_about_us(self, about_us_text):
        self.about_us = about_us_text
        self.dal_controller.website_repo.save(website_dto=self.to_dto())

    def get_contact_us(self):
        if not self.contact_info:
            return None
        return self.contact_info.to_dict()

    def set_contact_info(self, contact_info_dto):
        self.contact_info = contact_info_dto
        self.dal_controller.website_repo.save(website_dto=self.to_dto())

    def initial_approve_publication(self, publication_id) -> PublicationDTO:
        publication = self.get_publication_by_paper_id(publication_id)
        publication.approved = ApprovalStatus.FINAL_PENDING
        self.dal_controller.publications_repo.save(publication_dto=publication, domain=self.domain)
        return publication

    def get_all_initial_pending_publication(self):
        publications = self.dal_controller.publications_repo.find_by_domain(self.domain)
        return [pub for pub in publications if pub.approved == ApprovalStatus.INITIAL_PENDING]

    def get_all_final_pending_publication(self):
        publications = self.dal_controller.publications_repo.find_by_domain(self.domain)
        return [pub for pub in publications if pub.approved == ApprovalStatus.FINAL_PENDING]

    def reject_publication(self, publication_id) -> PublicationDTO:
        publication = self.get_publication_by_paper_id(publication_id)
        publication.approved = ApprovalStatus.REJECTED
        self.dal_controller.publications_repo.save(publication_dto=publication, domain=self.domain)
        return publication

    def add_news_record(self, news_record: NewsRecord_dto):
        """
        Adds a news record to the website's news list.
        """
        self.dal_controller.News_repo.save_news_record(news_record_dto=news_record)
    
    def to_dto(self) -> website_dto:
        return website_dto(
            domain=self.domain,
            contact_info=json.dumps(self.contact_info.to_dict()) if self.contact_info else "",
            about_us=self.about_us or ""
        )

    def set_news(self, news_list):
        self.news = news_list

    def get_news(self):
        return self.dal_controller.News_repo.find_news_by_domain(self.domain)
