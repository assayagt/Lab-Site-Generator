import Publication
class Website:
    def __init__(self, domain):
        self.members = []
        self.members_publications = {}
        self.domain = domain

    def create_publication(self, title, authors, date, approved, publication_link, media):
        # create new publicaiton and add it to the dictionary
        new_publication = Publication(title, authors, date, approved, publication_link, media)
        for author in authors:
            if author not in self.members_publications:
                self.members_publications[author] = []
            self.members_publications[author].append(new_publication)


    def check_publication_exist(self, publication):
        for member in self.members:
            if publication in self.members_publications[member]:
                return True
        return False