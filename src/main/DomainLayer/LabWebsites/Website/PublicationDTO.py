class PublicationDTO:
    def __init__(self, paper_id: str, title: str, authors: List[str],
                 publication_date: str, approved: bool,
                 publication_link: str, media: Optional[str] = None):

        self.paper_id = paper_id
        self.title = title
        self.authors = authors
        self.publication_date = publication_date
        self.approved = approved
        self.publication_link = publication_link
        self.media = media

    def to_dict(self):

        return {
            "paper_id": self.paper_id,
            "title": self.title,
            "authors": self.authors,
            "publication_date": self.publication_date,
            "approved": self.approved,
            "publication_link": self.publication_link,
            "media": self.media
        }
