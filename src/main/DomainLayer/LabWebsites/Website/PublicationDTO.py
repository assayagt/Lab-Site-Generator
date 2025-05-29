import uuid
from src.main.DomainLayer.LabWebsites.Website.ApprovalStatus import ApprovalStatus

class PublicationDTO:
    def __init__(self, title, publication_year, publication_link,
                 approved=ApprovalStatus.INITIAL_PENDING,
                 git_link=None, authors=None, video_link=None, presentation_link=None, description=None, paper_id=None, author_emails :list[str]=[], domain=None,
                 _scholarly_stub: dict = None, bibtex=None, arxiv_link=None):
        self.paper_id = str(uuid.uuid4()) if paper_id is None else paper_id
        self.title = title
        self.authors = authors 
        self.publication_year = publication_year
        # self.approved = approved.value if approved else None
        self.approved = approved
        self.publication_link = publication_link
        self.video_link = video_link
        self.git_link = git_link
        self.presentation_link = presentation_link
        self.description = description  # New description field
        self.author_emails = author_emails
        self.domain = domain
        self._scholarly_stub = _scholarly_stub # store the scholarly stub so we can refill it later
        self.bibtex = bibtex
        self.arxiv_link = arxiv_link
        


    def to_dict(self):
        return {
            "paper_id": self.paper_id,
            "title": self.title,
            "authors": self.authors,
            "publication_year": self.publication_year,
            "publication_link": self.publication_link,
            "video_link": self.video_link,
            "git_link": self.git_link,
            "presentation_link": self.presentation_link,
            "description": self.description , # Include description in dict
            "status" : self.approved.value,
            "domain": self.domain,
            "_scholarly_stub": self._scholarly_stub,
            "bibtex": self.bibtex,
            "arxiv": self.arxiv_link
        }

    def __eq__(self, other):
        # Equality check based only on title and year
        return (
                isinstance(other, PublicationDTO) and
                self.title.lower() == other.title.lower() and
                self.publication_year == other.publication_year
        )
    
    def __hash__(self):
        #override hash function as well to make sure sets and dictionaries work properly as well
        return hash((self.title.lower(), self.publication_year))
    
    def set_bibtex(self, bibtex):
        self.bibtex = bibtex

    def set_arxiv_link(self, arxiv_link):
        self.arxiv_link = arxiv_link

    def set_video_link(self, video_link):
        self.video_link = video_link

    def set_author_emails(self, author_emails):
        self.author_emails=  author_emails

    def set_git_link(self, git_link):
        self.git_link = git_link

    def set_presentation_link(self, presentation_link):
        self.presentation_link = presentation_link

    def set_description(self, description):
        """Set the description for the publication."""
        self.description = description

    def set_authors(self, authors):
        self.authors = authors

    def get_paper_id(self):
        return self.paper_id

    def get_authors(self):
        return self.authors

    def get_description(self):
        """Get the description of the publication."""
        return self.description
    
    def set_domain(self, domain):
        self.domain = domain
    
    def get_domain(self):
        return self.domain

    