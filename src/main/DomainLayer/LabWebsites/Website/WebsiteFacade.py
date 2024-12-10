class WebsiteFacade:
    def __init__(self):
        self.websites = []

    def add_website(self, website):
        self.websites.append(website)

    def get_website(self, domain):
        for website in self.websites:
            if website.domain == domain:
                return website
        return None

    def get_all_websites(self):
        return self.websites