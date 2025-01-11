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


    def check_publication_exist(self, publication):
        for author_publications in self.members_publications.values():
            for existing_publication in author_publications:
                # Compare the existing publication with the given publication
                if existing_publication == publication:
                    return True
        return False

    def get_all_approved_publication(self):
        approved_publications = []
        for publications in self.members_publications.values():  # Iterate over all author-publication lists
            for publication in publications:  # Iterate over publications for each author
                if publication.approved:  # Check if the publication is approved
                    approved_publications.append(publication)
        return approved_publications

    def check_if_publication_approved(self, publication_paper_id):
        for author_email in self.members_publications:
            for publication in self.members_publications[author_email]:
                if publication.get_paper_id() == publication_paper_id:
                    return publication.approved

    def get_all_approved_publications_of_member(self, email):
        approved_publications = []
        if email in self.members_publications:  # Check if the email exists in the dictionary
            for publication in self.members_publications[email]:  # Iterate through the member's publications
                if publication.approved:  # Check if the publication is approved
                    approved_publications.append(publication)
        return approved_publications

    def set_publication_video_link(self, publication_paper_id, video_link):
        for author_email in self.members_publications:
            for publication in self.members_publications[author_email]:
                if publication.get_paper_id() == publication_paper_id:
                    publication.set_video_link(video_link)
                    return

    def set_publication_git_link(self, publication_paper_id, git_link):
        for author_email in self.members_publications:
            for publication in self.members_publications[author_email]:
                if publication.get_paper_id() == publication_paper_id:
                    publication.set_git_link(git_link)
                    return

    def set_publication_presentation_link(self, publication_paper_id):
        for author_email in self.members_publications:
            for publication in self.members_publications[author_email]:
                if publication.get_paper_id() == publication_paper_id:
                    publication.set_presentation_link()
                    return

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

    def final_approve_publication(self, paper_id):
        publication = self.get_publication_by_paper_id(paper_id)
        publication.approved = True

    def get_domain(self):
        return self.domain

    def get_about_us(self):
        return self.about_us

    def set_about_us(self, about_us_text):
        self.about_us = about_us_text

    def set_contact_info(self, contact_info_dto):
        self.contact_info = contact_info_dto