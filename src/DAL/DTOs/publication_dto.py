import uuid

class publication_dto:
    def __init__(self, title, authors,
                 publication_year, approved,
                 publication_link, git_link=None, video_link=None, presentation_link=None, description=None):

        self.paper_id = str(uuid.uuid4())
        self.title = title
        self.authors = authors
        self.publication_year = publication_year
        self.approved = approved
        self.publication_link = publication_link
        self.video_link = video_link
        self.git_link = git_link
        self.presentation_link = presentation_link
        self.description = description  # New description field

    def get_json(self):
        return {
            "paper_id": self.paper_id,
            "title": self.title,
            "authors": self.authors,
            "publication_year": self.publication_year,
            "publication_link": self.publication_link,
            "video_link": self.video_link,
            "git_link": self.git_link,
            "presentation_link": self.presentation_link,
            "description": self.description  # Include description in dict
        }