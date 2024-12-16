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

    def crawl_for_publications(self):
        # get list of all websites
        websites = get_all_websites()

        # for each website, send to the webCrawler facade the members and current year to fetch publications
        publications = []
        for website in websites:
            publications.extend(WebCrawlerFacade().fetch_publications(website.members, datetime.now().year))

            # check that each publication is not already in website members publications
            for publication in publications:
                if website.check_publication_exist(publication):
                    publications.remove(publication)


            #TODO : After sending the notifications to the website members, add the new publications to the website
            # For now, assume that the publications are already sent to the website members

            #add the new publications to the website
            for publication in publications:
                website.create_publication(publication.title, publication.authors, publication.date, publication.approved, publication.publication_link, publication.media)