from typing import List, Dict
from datetime import datetime

class Publication:
    def __init__(self, title, authors, date,
                 approved, publication_link, media):
        self.title = title
        self.authors = authors
        self.date = date
        self.approved = approved
        self.publication_link = publication_link