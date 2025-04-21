import time
from bs4 import BeautifulSoup
from scholarly import scholarly

from src.main.DomainLayer.LabWebsites.Website.ApprovalStatus import ApprovalStatus
from src.main.DomainLayer.LabWebsites.Website.PublicationDTO import PublicationDTO
import requests

class GoogleScholarWebCrawler:
    def __init__(self):
        self.visited_papers = set()

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

                        publication_description = self.get_description_from_citation(url)

                        publication_dto = PublicationDTO(
                            title=new_publication_title,
                            authors=publication_authors,
                            publication_year=pub_year,
                            approved=ApprovalStatus.INITIAL_PENDING.value,  # Default value
                            publication_link=url,
                            description=publication_description
                        )


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


    def get_details_by_link(self, link):
        try:
            # Fetch the page content
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(link, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            soup = BeautifulSoup(response.text, "html.parser")

            # Extract authors
            authors_section = soup.find("div", class_="gsc_oci_value")
            authors = [author.strip() for author in authors_section.text.split(",")] if authors_section else []

            # Extract title
            title_section = soup.find("a", class_="gsc_oci_title_link")
            title = title_section.text.strip() if title_section else "Title not found"

            # Extract publication year
            year_section = soup.find("div", text="Publication date")
            year = (
                year_section.find_next_sibling("div").text.strip()
                if year_section
                else "Year not found"
            )

            description = self.get_description_from_citation(link)

            return {
                "authors": authors,
                "title": title,
                "publication_year": year,
                "description": description,
            }

        except Exception as e:
            print(f"Error occurred: {e}")
            return {}

    def get_description_from_citation(self, url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            description_section = soup.find("div", class_="gsc_oci_value", id="gsc_oci_descr")
            if description_section:
                return description_section.get_text(separator=" ").strip()  # Clean up the text
            else:
                return "Description not available"

        except Exception as e:
            print(f"Error occurred: {e}")
            return "Error fetching description"

