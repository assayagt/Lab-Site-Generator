class ScannedPublication:
    def __init__(self, title, publication_year, scholar_id, author_pub_id):
        self.title = title
        self.publication_year = publication_year
        self.scholar_id = scholar_id
        self.author_pub_id = author_pub_id  # explicitly save author_pub_id for clarity

    def build_publication_url(self):
        """
        Build the Google Scholar citation URL for this publication.
        """
        return f"https://scholar.google.com/citations?view_op=view_citation&hl=en&user={self.scholar_id}&citation_for_view={self.author_pub_id}"
