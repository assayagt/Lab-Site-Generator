import time
from bs4 import BeautifulSoup
from scholarly import scholarly

from src.main.DomainLayer.LabWebsites.Website.ApprovalStatus import ApprovalStatus
from src.main.DomainLayer.LabWebsites.Website.PublicationDTO import PublicationDTO
from src.main.DomainLayer.LabWebsites.WebCrawler.ScannedPublication import ScannedPublication
from src.DAL.DAL_controller import DAL_controller
import requests

class GoogleScholarWebCrawler:
    def __init__(self):
        self.crawled = {} #{domain, [scanned_pubs]}
        self.dal_controller = DAL_controller()
        self._load_scanned_pubs()

    def fetch_publications_new_member(self, authors, domain):
        """
        Fetches publications from Google Scholar for the given authors.

        Args:
            authors (list): List of author names to search for.
        """
        scanned_pubs = []
        for author_name in authors:
            search_query = scholarly.search_author(author_name)
            author = next(search_query, None)

            if author:
                author = scholarly.fill(author)
                for publication in author.get("publications", []):
                    # Create a ScannedPublication object
                    publication_title = publication.get("bib", {}).get("title")
                    publication_year = publication.get("bib", {}).get("pub_year")
                    scholar_id = author.get("scholar_id")
                    author_pub_id = publication['author_pub_id']
                    scanned_publication = ScannedPublication(
                        title=publication_title,
                        publication_year=publication_year,
                        scholar_id=scholar_id,
                        author_pub_id=author_pub_id
                    )

                    scanned_pubs.append(scanned_publication)
            # Add a delay to avoid overwhelming the server
            time.sleep(30)


        #if domain exists in self.crawled, append the new publications
        #if domain does not exist in self.crawled, create a new entry
        if domain in self.crawled:
            self.crawled[domain].extend(scanned_pubs)
        else:
            self.crawled[domain] = scanned_pubs
        # ========================================= SAVE TO DATA =========================================
        for scanned_pub in self.crawled[domain]:
            self.dal_controller.publications_repo.save_scanned_pub(scannedPub=scanned_pub.to_dto(), domain=domain)


    def fetch_crawler_publications(self, authors, domain):
        results = []
        scanned_pubs = self.crawled.get(domain, [])
        for author_name in authors:
            search_query = scholarly.search_author(author_name)
            author = next(search_query, None)

            author = scholarly.fill(author)

            for publication in author.get("publications", []):
                new_publication_title = publication.get("bib", {}).get("title")

                if new_publication_title and not any(pub.title == new_publication_title for pub in scanned_pubs):
                    # Create a ScannedPublication object
                    publication_title = publication.get("bib", {}).get("title")
                    publication_year = publication.get("bib", {}).get("pub_year")
                    scholar_id = author.get("scholar_id")
                    author_pub_id = publication['author_pub_id']
                    scanned_publication = ScannedPublication(
                        title=publication_title,
                        publication_year=publication_year,
                        scholar_id=scholar_id,
                        author_pub_id=author_pub_id
                    )
                    url = scanned_publication.build_publication_url()

                    publication_authors = self.get_authors_from_citation(url)

                    publication_description = self.get_description_from_citation(url)

                    pub_year = publication.get("bib", {}).get("pub_year")

                    publication_dto = PublicationDTO(
                        title=new_publication_title,
                        authors=publication_authors,
                        publication_year=pub_year,
                        approved=ApprovalStatus.INITIAL_PENDING.value,  # Default value
                        publication_link=url,
                        description=publication_description
                    )

                    self.crawled[domain].append(scanned_publication)  # Add to crawled publications
                    # ========================================= SAVE TO DATA =========================================
                    self.dal_controller.publications_repo.save_scanned_pub(scannedPub=scanned_publication.to_dto(), domain=domain) 
                    results.append(publication_dto)

        #add 30 seconds delay
        time.sleep(30)

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
        

    def _load_scanned_pubs(self):
        domainList = self.dal_controller.publications_repo.find_all_domains_with_scannedPubs()
        for domain in domainList:
            pubList = self.dal_controller.publications_repo.find_scanned_pubs_by_domain(domain)
            if domain in self.crawled:
                self.crawled[domain].extend(pubList)
            else:
                self.crawled[domain] = [pubList]
            

