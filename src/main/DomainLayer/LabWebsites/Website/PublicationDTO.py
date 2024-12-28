class PublicationDTO:
    def __init__(self, paper_id, title, authors,
                 publication_year, approved,
                 publication_link, video_link=None, git_link=None, presentation_link=None):

        self.paper_id = paper_id
        self.title = title
        self.authors = authors
        self.publication_year = publication_year
        self.approved = approved
        self.publication_link = publication_link
        self.video_link = video_link
        self.git_link = git_link
        self.presentation_link = presentation_link

    def to_dict(self):

        return {
            "paper_id": self.paper_id,
            "title": self.title,
            "authors": self.authors,
            "publication_year": self.publication_year,
            "approved": self.approved,
            "publication_link": self.publication_link,
            "video_link": self.video_link,
            "git_link": self.git_link,
            "presentation_link": self.presentation_link
        }

    def __eq__(self, other):
        # Equality check based only on title and year
        return (
                isinstance(other, PublicationDTO) and
                self.title.lower() == other.title.lower() and
                self.publication_year == other.publication_year
        )

    def set_video_link(self, video_link):
        self.video_link = video_link

    def set_git_link(self, git_link):
        self.git_link = git_link

    def set_presentation_link(self, presentation_link):
        self.presentation_link = presentation_link

    def get_paper_id(self):
        return self.paper_id

