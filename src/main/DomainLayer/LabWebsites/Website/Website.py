from src.main.DomainLayer.LabWebsites.Website.ApprovalStatus import ApprovalStatus
from src.main.DomainLayer.LabWebsites.Website.PublicationDTO import PublicationDTO
from src.DAL.DTOs.Website_dto import website_dto
import json

class Website:
    def __init__(self, domain, contact_info=None, about_us=None):
        self.members_publications = {}
        self.domain = domain
        self.contact_info = contact_info
        self.about_us = about_us

    def create_publication(self, publicationDTO, authors_emails):
        # get new publicationDTO and add it to the dictionary
        for author_email in authors_emails:
            if author_email not in self.members_publications:
                self.members_publications[author_email] = []
            self.members_publications[author_email].append(publicationDTO)
            

    def add_publication_manually(self, publication_link, publication_details, git_link, video_link, presentation_link,
                                 authors_emails) -> PublicationDTO:
        publication_dto = PublicationDTO(publication_details["title"], publication_details["authors"],
                                         publication_details["publication_year"], ApprovalStatus.FINAL_PENDING.value,
                                         publication_link, git_link, video_link, presentation_link,
                                         publication_details["description"])
        self.create_publication(publication_dto, authors_emails)
        return publication_dto


    def check_publication_exist(self, publication):
        for author_publications in self.members_publications.values():
            for existing_publication in author_publications:
                # Compare the existing publication with the given publication
                if existing_publication == publication:
                    return True
        return False

    def get_all_approved_publication(self):
        approved_publications = []
        seen_paper_ids = set()  # To track unique paper IDs

        for publications in self.members_publications.values():  # Iterate over all author-publication lists
            for publication in publications:  # Iterate over publications for each author
                if publication.approved == ApprovalStatus.APPROVED.value and publication.get_paper_id() not in seen_paper_ids:
                    approved_publications.append(publication.to_dict())
                    seen_paper_ids.add(publication.get_paper_id())  # Mark the paper ID as seen

        return approved_publications

    def check_if_publication_approved(self, publication_paper_id):
        for author_email in self.members_publications:
            for publication in self.members_publications[author_email]:
                if publication.get_paper_id() == publication_paper_id:
                    return publication.approved == ApprovalStatus.APPROVED.value
                    

    def get_all_approved_publications_of_member(self, email):
        approved_publications = []
        if email in self.members_publications:  # Check if the email exists in the dictionary
            for publication in self.members_publications[email]:  # Iterate through the member's publications
                if publication.approved == ApprovalStatus.APPROVED.value:  # Check if the publication is approved
                    approved_publications.append(publication.to_dict())
        return approved_publications

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

    def check_if_member_is_publication_author(self, email, publication_paper_id):
        if email in self.members_publications:
            for publication in self.members_publications[email]:
                if publication.get_paper_id() == publication_paper_id:
                    return True
        return False

    def get_publication_by_paper_id(self, paper_id):
        for author_email in self.members_publications:
            for publication in self.members_publications[author_email]:
                if publication.get_paper_id() == paper_id:
                    return publication
        return None

    def final_approve_publication(self, paper_id) -> PublicationDTO:
        publication = self.get_publication_by_paper_id(paper_id)
        publication.approved = ApprovalStatus.APPROVED.value
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
        publication.approved = ApprovalStatus.FINAL_PENDING.value
        return publication

    def get_all_initial_pending_publication(self):
        initial_publications = []
        seen_paper_ids = set()  # To track unique paper IDs

        for publications in self.members_publications.values():  # Iterate over all author-publication lists
            for publication in publications:  # Iterate over publications for each author
                if publication.approved == ApprovalStatus.INITIAL_PENDING.value and publication.get_paper_id() not in seen_paper_ids:
                    initial_publications.append(publication)
                    seen_paper_ids.add(publication.get_paper_id())  # Mark the paper ID as seen

        return initial_publications

    def get_all_final_pending_publication(self):
        final_publications = []
        seen_paper_ids = set()  # To track unique paper IDs

        for publications in self.members_publications.values():  # Iterate over all author-publication lists
            for publication in publications:  # Iterate over publications for each author
                if publication.approved == ApprovalStatus.INITIAL_PENDING.value and publication.get_paper_id() not in seen_paper_ids:
                    final_publications.append(publication)
                    seen_paper_ids.add(publication.get_paper_id())  # Mark the paper ID as seen

        return final_publications

    def reject_publication(self, publication_id) -> PublicationDTO:
        publication = self.get_publication_by_paper_id(publication_id)
        publication.approved = ApprovalStatus.REJECTED.value
        return publication
    
    def to_dto(self) -> website_dto:
        return website_dto(
            domain=self.domain,
            contact_info=json.dumps(self.contact_info.to_dict()) if self.contact_info else None,
            about_us=self.about_us
        )

    def load_pub_dtos(self, pub_list: list[PublicationDTO]):
        for pub in pub_list:
            for author in pub.author_emails:
                if author not in self.members_publications:
                    self.members_publications[author] = []
                self.members_publications[author].append(pub)