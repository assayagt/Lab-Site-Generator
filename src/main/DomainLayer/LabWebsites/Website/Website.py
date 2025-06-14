from src.main.DomainLayer.LabWebsites.Website.ApprovalStatus import ApprovalStatus
from src.main.DomainLayer.LabWebsites.Website.PublicationDTO import PublicationDTO
from src.DAL.DTOs.Website_dto import website_dto
from src.DAL.DTOs.NewsRecord_dto import NewsRecord_dto
from src.main.Util.ExceptionsEnum import ExceptionsEnum
from src.DAL.DAL_controller import DAL_controller
import json

class Website:
    def __init__(self, domain, contact_info=None, about_us=None):
        self.members_publications: dict[str, list[PublicationDTO]] = {} #=================== LAZY LOAD THAT (?)
        self.domain = domain
        self.contact_info = contact_info
        self.about_us = about_us
        self.news: list[NewsRecord_dto] = [] #=================== LAZY LOAD THAT

    def create_publication(self, publicationDTO, authors_emails):
        # get new publicationDTO and add it to the dictionary
        for author_email in authors_emails:
            if author_email not in self.members_publications:
                self.members_publications[author_email] = []
            if publicationDTO not in self.members_publications[author_email]:
                self.members_publications[author_email].append(publicationDTO)
            else:
                for pub in self.members_publications[author_email]:
                    if pub == publicationDTO:
                        if pub.approved == ApprovalStatus.APPROVED:
                            raise Exception(ExceptionsEnum.PUBLICATION_ALREADY_APPROVED.value)
                        else:
                            raise Exception(ExceptionsEnum.PUBLICATION_ALREADY_WAITING.value)
        print("publication added to website succesffully")

    def update_publication(self, publicationDTO: PublicationDTO):
        # Remove any existing entries equal to publicationDTO
        for author_email, pubs in list(self.members_publications.items()):
            # filter out old instances
            new_list = [p for p in pubs if p != publicationDTO]
            if new_list:
                self.members_publications[author_email] = new_list
            else:
                # no publications left for this email → remove the key
                del self.members_publications[author_email]

        # Re-add the updated DTO under its current authors
        self.create_publication(publicationDTO, publicationDTO.author_emails)
                    
            

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
        for author_publications in self.members_publications.values():
            if publication in author_publications:
                    return True
        return False

    def get_all_approved_publication(self):
        approved_publications = []
        seen_paper_ids = set()  # To track unique paper IDs

        for publications in self.members_publications.values():  # Iterate over all author-publication lists
            for publication in publications:  # Iterate over publications for each author
                if publication.approved == ApprovalStatus.APPROVED and publication.get_paper_id() not in seen_paper_ids:
                    approved_publications.append(publication.to_dict())
                    seen_paper_ids.add(publication.get_paper_id())  # Mark the paper ID as seen

        return approved_publications
    
    def get_all_not_approved_publications(self):
        pubs = set()
        for publications in self.members_publications.values():
            for publication in publications:
                if publication.approved != ApprovalStatus.APPROVED.value:
                    pubs.add(publication)
        return list(pubs)

    def check_if_publication_approved(self, publication_paper_id):
        for author_email in self.members_publications:
            for publication in self.members_publications[author_email]:
                if publication.get_paper_id() == publication_paper_id:
                    return publication.approved == ApprovalStatus.APPROVED
                    

    def get_all_approved_publications_of_member(self, email):
        approved_publications = []
        if email in self.members_publications:  # Check if the email exists in the dictionary
            for publication in self.members_publications[email]:  # Iterate through the member's publications
                if publication.approved == ApprovalStatus.APPROVED:  # Check if the publication is approved
                    approved_publications.append(publication.to_dict())
        return approved_publications
    
    def get_all_not_approved_publications_of_member(self, email):
        pubs = []
        if email in self.members_publications:
            for pub in self.members_publications[email]:
                if pub.approved != ApprovalStatus.APPROVED.value:
                    pubs.append(pub.to_dict())
        return pubs

    def set_publication_video_link(self, publication_paper_id, video_link) -> PublicationDTO:
        for author_email in self.members_publications:
            for publication in self.members_publications[author_email]:
                if publication.get_paper_id() == publication_paper_id:
                    publication.set_video_link(video_link)
                    return publication

    def set_publication_git_link(self, publication_paper_id, git_link) -> PublicationDTO:
        for author_email in self.members_publications:
            for publication in self.members_publications[author_email]:
                if publication.get_paper_id() == publication_paper_id:
                    publication.set_git_link(git_link)
                    return publication

    def set_publication_presentation_link(self, publication_paper_id,link) -> PublicationDTO:
        for author_email in self.members_publications:
            for publication in self.members_publications[author_email]:
                if publication.get_paper_id() == publication_paper_id:
                    publication.set_presentation_link(link)
                    return publication

    def check_if_member_is_publication_author(self,publication_paper_id, email):
        if email in self.members_publications:
            for publication in self.members_publications[email]:
                if publication.get_paper_id() == publication_paper_id:
                    return True
        return False

    def get_publication_by_paper_id(self, paper_id) -> PublicationDTO:
        for pub_list in self.members_publications.values():
            for publication in pub_list:
                if publication.get_paper_id() == paper_id:
                    return publication
        
        # # Lazy-load from DB if not found (we don't do that anymore)
        # publication = DAL_controller().publications_repo.find_by_id(paper_id=paper_id)
        # if publication:
        #     for author in publication.author_emails:
        #         if author not in self.members_publications:
        #             self.members_publications[author] = []
        #         if publication not in self.members_publications[author]:
        #             self.members_publications[author].append(publication)
        #     return publication
        return None
    
    def is_publication_rejected(self, paper_id):
        return self.get_publication_by_paper_id(paper_id=paper_id).approved == ApprovalStatus.REJECTED

    def final_approve_publication(self, paper_id) -> PublicationDTO:
        publication = self.get_publication_by_paper_id(paper_id)
        publication.approved = ApprovalStatus.APPROVED
        return publication

    def get_domain(self):
        return self.domain

    def get_about_us(self):
        return self.about_us

    def set_about_us(self, about_us_text):
        self.about_us = about_us_text

    def get_contact_us(self):
        return self.contact_info.to_dict()

    def set_contact_info(self, contact_info_dto):
        self.contact_info = contact_info_dto

    def initial_approve_publication(self, publication_id) -> PublicationDTO:
        publication = self.get_publication_by_paper_id(publication_id)
        publication.approved = ApprovalStatus.FINAL_PENDING
        return publication

    def get_all_initial_pending_publication(self):
        initial_publications = []
        seen_paper_ids = set()  # To track unique paper IDs

        for publications in self.members_publications.values():  # Iterate over all author-publication lists
            for publication in publications:  # Iterate over publications for each author
                if publication.approved == ApprovalStatus.INITIAL_PENDING and publication.get_paper_id() not in seen_paper_ids:
                    initial_publications.append(publication)
                    seen_paper_ids.add(publication.get_paper_id())  # Mark the paper ID as seen

        return initial_publications

    def get_all_final_pending_publication(self):
        final_publications = []
        seen_paper_ids = set()  # To track unique paper IDs

        for publications in self.members_publications.values():  # Iterate over all author-publication lists
            for publication in publications:  # Iterate over publications for each author
                if publication.approved == ApprovalStatus.INITIAL_PENDING and publication.get_paper_id() not in seen_paper_ids:
                    final_publications.append(publication)
                    seen_paper_ids.add(publication.get_paper_id())  # Mark the paper ID as seen

        return final_publications

    def reject_publication(self, publication_id) -> PublicationDTO:
        publication = self.get_publication_by_paper_id(publication_id)
        publication.approved = ApprovalStatus.REJECTED
        return publication

    def add_news_record(self, news_record: NewsRecord_dto):
        """
        Adds a news record to the website's news list.
        """
        self.news.append(news_record)
    
    def to_dto(self) -> website_dto:
        return website_dto(
            domain=self.domain,
            contact_info=json.dumps(self.contact_info.to_dict()) if self.contact_info else None,
            about_us=self.about_us
        )
    
    def load_author_publications(self, author_email: str):
        if author_email in self.members_publications:
            return
        pub_list = DAL_controller().publications_repo.find_by_author_email(author_email, self.domain)
        self.members_publications[author_email] = pub_list

    def reload_all_publications(self):
        self.members_publications.clear()
        pub_list = DAL_controller().publications_repo.find_by_domain(self.domain)
        self.load_pub_dtos(pub_list)

    def clear_publications(self):
        self.members_publications.clear()

    def load_pub_dtos(self, pub_list: list[PublicationDTO]):
        for pub in pub_list:
            for author in pub.author_emails:
                if author not in self.members_publications:
                    self.members_publications[author] = []
                self.members_publications[author].append(pub)

    def set_news(self, news_list):
        self.news = news_list

    def get_news(self):
        return self.news
