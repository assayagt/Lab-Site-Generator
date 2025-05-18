import time
import re
from bs4 import BeautifulSoup
from scholarly import scholarly

from src.main.DomainLayer.LabWebsites.Website.ApprovalStatus import ApprovalStatus
from src.main.DomainLayer.LabWebsites.Website.PublicationDTO import PublicationDTO
# from src.main.DomainLayer.LabWebsites.WebCrawler.ScannedPublication import ScannedPublication
# from src.DAL.DAL_controller import DAL_controller
import requests

class GoogleScholarWebCrawler:
    def __init__(self):
        """Initialize MyClass (no attributes by default)."""
        pass


    # (was) def fetch_publications_new_member(self, scholar_ids, domain):
    def fetch_crawler_publications(self, scholarLinks) -> list[PublicationDTO]: # type: ignore
        """
        Fetches publications from Google Scholar for the given list of scholar IDs.

        Args:
            scholar_ids (list): List of scholar IDs for the authors.         
        """
        crawled: list[PublicationDTO] = []
        for link in scholarLinks:
            scholar_id = self.extract_scholar_id(link)
            try:
                # Fetch author by scholar_id
                author_gen = scholarly.search_author(scholar_id)
                author = next(author_gen)
                author = scholarly.fill(author)

                for pub in author.get("publications", []):
                    pub_title = pub.get("bib", {}).get("title")
                    pub_year = pub.get("bib", {}).get("pub_year")
                    author_pub_id = pub.get("author_pub_id")
                    if pub_title is None or pub_year is None:
                        print(f"GOOGLE CRAWLER => publication title or year found empty")
                        continue 
                    key = (pub_title, pub_year)
                    if key in crawled:
                        print(f"GOOGLE CRAWLER => title: {pub_title} and year: {pub_year} appears more than once!")
                        continue
                    else:
                        # New publication -> create new pub
                        url = self.build_publication_url(scholar_id=scholar_id, author_pub_id=author_pub_id)
                        new_pub = PublicationDTO(
                            title= pub_title,
                            publication_year= pub_year,
                            publication_link= url,
                            approved=ApprovalStatus.INITIAL_PENDING.value
                        )
                        crawled.append(new_pub)
                time.sleep(1) #we might replace it to 1 bc scholarly already has a built-in delay mechanism
                return crawled
            except Exception as e:
                print(f"Error fectching publications for scholar_id {scholar_id}: {e}")
                return []
        

    def fill_details(self, publicationDTOs: list[PublicationDTO]):
        """
        This method accepts a list of PublicationDTO and fills description and authors into it
        """
        for pub in publicationDTOs:
            url = pub.publication_link
            if url:
                pub.set_description(self.get_description_from_citation(url))
                pub.set_authors(self.get_authors_from_citation(url))
                
       

    # def fetch_crawler_publications(self, authors, domain):
    #     results = []
    #     scanned_pubs = self.crawled.get(domain, [])
    #     for author_name in authors:
    #         search_query = scholarly.search_author(author_name)
    #         author = next(search_query, None)

    #         author = scholarly.fill(author)

    #         for publication in author.get("publications", []):
    #             new_publication_title = publication.get("bib", {}).get("title")

    #             if new_publication_title and not any(pub.title == new_publication_title for pub in scanned_pubs):
    #                 # Create a ScannedPublication object
    #                 publication_title = publication.get("bib", {}).get("title")
    #                 publication_year = publication.get("bib", {}).get("pub_year")
    #                 scholar_id = author.get("scholar_id")
    #                 author_pub_id = publication['author_pub_id']
    #                 scanned_publication = ScannedPublication(
    #                     title=publication_title,
    #                     publication_year=publication_year,
    #                     scholar_id=scholar_id,
    #                     author_pub_id=author_pub_id
    #                 )
    #                 url = scanned_publication.build_publication_url()

    #                 publication_authors = self.get_authors_from_citation(url)

    #                 publication_description = self.get_description_from_citation(url)

    #                 pub_year = publication.get("bib", {}).get("pub_year")

    #                 publication_dto = PublicationDTO(
    #                     title=new_publication_title,
    #                     authors=publication_authors,
    #                     publication_year=pub_year,
    #                     approved=ApprovalStatus.INITIAL_PENDING.value,  # Default value
    #                     publication_link=url,
    #                     description=publication_description
    #                 )

    #                 self.crawled[domain].append(scanned_publication)  # Add to crawled publications
    #                 # ========================================= SAVE TO DATA =========================================
    #                 self.dal_controller.publications_repo.save_scanned_pub(scannedPub=scanned_publication, domain=domain) 
    #                 results.append(publication_dto)

    #     #add 30 seconds delay
    #     time.sleep(5)

    #     return results
    
    def build_publication_url(self, scholar_id, author_pub_id):
        """
        Build the Google Scholar citation URL for this publication.
        """
        return f"https://scholar.google.com/citations?view_op=view_citation&hl=en&user={scholar_id}&citation_for_view={author_pub_id}"

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
        
    def extract_scholar_id(self, profile_link: str) -> str:
        """
        Extracts scholar ID from a Google Scholar profile link using regex.
        """
        match = re.search(r"user=([\w-]+)", profile_link)
        if match:
            return match.group(1)
        return ""
        

    # def _load_scanned_pubs(self):
    #     domain_list = self.dal_controller.publications_repo.find_all_domains_with_scannedPubs()
    #     for domain in domain_list:
    #         pub_list = self.dal_controller.publications_repo.find_scanned_pubs_by_domain(domain)  # → list of ScannedPublication
    #         if domain not in self.crawled:
    #             self.crawled[domain] = {}
    #         domain_pubs = self.crawled[domain]

    #         # Add each publication into the dict with key (title, year)
    #         for pub in pub_list:
    #             key = (pub.title, pub.publication_year)
    #             domain_pubs[key] = pub

