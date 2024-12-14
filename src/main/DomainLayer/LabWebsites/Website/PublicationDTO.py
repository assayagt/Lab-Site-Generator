class PublicationDTO:
    def __init__(self, paper_id, title, authors,
                 publication_year, approved,
                 publication_link, media):

        self.paper_id = paper_id
        self.title = title
        self.authors = authors
        self.publication_year = publication_year
        self.approved = approved
        self.publication_link = publication_link
        self.media = media

    def to_dict(self):

        return {
            "paper_id": self.paper_id,
            "title": self.title,
            "authors": self.authors,
            "publication_year": self.publication_year,
            "approved": self.approved,
            "publication_link": self.publication_link,
            "media": self.media
        }

    def __eq__(self, other):
        # Equality check based only on title and year
        return (
                isinstance(other, PublicationDTO) and
                self.title.lower() == other.title.lower() and
                self.publication_year == other.publication_year
        )