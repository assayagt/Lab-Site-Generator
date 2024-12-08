import Publication
class Website:
    def __init__(self, domain):
        self.members_publications = {}
        self.domain = domain

    def create_publication(self, title, authors, date, approved, publication_link, media):
        # create new publicaiton and add it to the dictionary
        new_publication = Publication(title, authors, date, approved, publication_link, media)
        for author in authors:
            if author not in self.members_publications:
                self.members_publications[author] = []
            self.members_publications[author].append(new_publication)

    def verify_publication_not_blacklisted(self, publication_dto: Publication):
        # Check if the publication exists in the system (in the members_publications list)
        for publications in self.members_publications.values():
            for publication in publications:
                if publication.title == publication_dto.title and publication.date == publication_dto.date:
                    if not publication.approved:
                        return False
        # If the publication is not found or is approved, return True (not blacklisted)
        return True
