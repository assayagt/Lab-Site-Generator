from datetime import time

from bs4 import BeautifulSoup
from scholarly import scholarly
from src.main.DomainLayer.LabWebsites.Website import PublicationDTO
import requests

class GoogleScholarWebCrawler:
    def __init__(self):
        self.visited_papers = set()
        self.id_counter = 0 # needed for the paper_id, WILL BE REMOVED IN THE FUTURE

    def fetch_crawler_publications(self, authors, year):
        results = []

        for author_name in authors:
            search_query = scholarly.search_author(author_name)
            author = next(search_query, None)

            author = scholarly.fill(author)

            for publication in author.get("publications", []):
                pub_year = publication.get("bib", {}).get("pub_year")

                if pub_year and int(pub_year) == year:
                    new_publication_title = publication.get("bib", {}).get("title")

                    if new_publication_title and not any(pub.title == new_publication_title for pub in self.visited_papers):

                        scholar_id = author.get("scholar_id")

                        url = f"https://scholar.google.com/citations?view_op=view_citation&hl=en&user={scholar_id}&citation_for_view={publication['author_pub_id']}"

                        publication_authors = self.get_authors_from_citation(url)

                        publication_dto = PublicationDTO(
                            paper_id=self.id_counter,
                            title=new_publication_title,
                            authors=publication_authors,
                            publication_year=pub_year,
                            approved=False,  # Default value
                            publication_link=url,
                            media=None
                        )

                        self.id_counter += 1

                        self.visited_papers.add(publication_dto)
                        results.append(publication_dto)

            #add 60 seconds delay
            time.sleep(60)

        return results

    def get_authors_from_citation(self, url):
        try:
            # Fetch the page content
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            soup = BeautifulSoup(response.text, "html.parser")

            authors_section = soup.find("div", class_="gsc_oci_value")
            if authors_section:
                authors = [author.strip() for author in authors_section.text.split(",")]
                return authors
            else:
                return []

        except Exception as e:
            print(f"Error occurred: {e}")
            return []