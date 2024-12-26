from PublicationDTO import PublicationDTO
class Website:
    def __init__(self, domain):
        self.members_publications = {}
        self.domain = domain

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

    def get_all_approved_publications_of_member(self, email):
        approved_publications = []
        if email in self.members_publications:  # Check if the email exists in the dictionary
            for publication in self.members_publications[email]:  # Iterate through the member's publications
                if publication.approved:  # Check if the publication is approved
                    approved_publications.append(publication)
        return approved_publications
