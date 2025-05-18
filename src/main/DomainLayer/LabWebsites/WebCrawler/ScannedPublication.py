class ScannedPublication:
    def __init__(self, title, publication_year, scholar_id, author_pub_id, is_published = False):
        self.title = title
        self.publication_year = publication_year
        self.scholar_N_author_pub_id = [(scholar_id, author_pub_id)]
        self.is_published = is_published


    def set_is_published(self, is_published):
        self.is_published = is_published

    def add_scholar_N_author_pub_id(self, scholar_id, author_pub_id):
        self.scholar_N_author_pub_id.append((scholar_id, author_pub_id))

    def build_publication_url(self):
        """
        Build the Google Scholar citation URL for this publication.
        """
        scholar_id, author_pub_id = self.scholar_N_author_pub_id[0]
        return f"https://scholar.google.com/citations?view_op=view_citation&hl=en&user={scholar_id}&citation_for_view={author_pub_id}"
