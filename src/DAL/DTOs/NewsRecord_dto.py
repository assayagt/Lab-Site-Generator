from datetime import datetime

class NewsRecord_dto:
    def __init__(self, id, domain, text, link=None, date=None):

        self.domain = domain
        self.id = id
        self.text = text
        self.link = link
        #make date to be today's date if not provided
        if isinstance(date, str):
            self.date = datetime.fromisoformat(date)
        else:
            self.date = date

    def get_id(self):
        return self.id

    def get_domain(self):
        return self.domain

    def get_text(self):
        return self.text

    def get_link(self):
        return self.link

    def set_text(self, text):
        self.text = text

    def set_link(self, link):
        self.link = link

    def get_json(self):
        return {
            "id": self.id,
            "domain": self.domain,
            "text": self.text,
            "link": self.link,
            "date" : self.date
        }