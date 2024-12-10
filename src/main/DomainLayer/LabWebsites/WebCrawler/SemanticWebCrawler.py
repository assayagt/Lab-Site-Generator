import requests
from typing import List

class SemanticWebCrawler(WebCrawler):
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited_papers = set()  # Cache to store visited paper IDs

    def fetch_crawler_publications(self, authors, year):
        """
        Fetches publications for the given authors and year from the Semantic Scholar API.
        Returns a list of PublicationDTO instances.
        """
        results = []

        for author in authors:
            search_url = f"{self.base_url}/author/search"
            params = {"query": author, "fields": "name,papers"}
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("data"):
                for author_data in data["data"]:
                    for paper in author_data.get("papers", []):
                        paper_id = paper.get("paperId")
                        if paper_id and paper_id not in self.visited_papers:
                            # Add the paper ID to the cache
                            self.visited_papers.add(paper_id)
                            if paper.get("year") == year:
                                # Extracting all authors from the paper
                                paper_authors = [a.get("name", "Unknown") for a in paper.get("authors", [])]

                                publication = PublicationDTO(
                                    paper_id=paper_id,
                                    title=paper.get("title"),
                                    authors=paper_authors,
                                    publication_date=f"{paper.get('year')}-01-01",  # Default to Jan 1 if only year available
                                    approved=False,  # Default value
                                    publication_link=paper.get("url"),
                                    media=None
                                )
                                results.append(publication)

        return results
