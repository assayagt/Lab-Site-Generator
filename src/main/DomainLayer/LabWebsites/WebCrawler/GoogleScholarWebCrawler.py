import time
import re
from bs4 import BeautifulSoup 
from scholarly import scholarly
from urllib.parse import urljoin
from datetime import datetime
from src.main.DomainLayer.LabWebsites.Website.ApprovalStatus import ApprovalStatus
from src.main.DomainLayer.LabWebsites.Website.PublicationDTO import PublicationDTO
# from src.main.DomainLayer.LabWebsites.WebCrawler.ScannedPublication import ScannedPublication
# from src.DAL.DAL_controller import DAL_controller
import requests, threading

class GoogleScholarWebCrawler:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if getattr(self, "_inited", False):
            return
        """Initialize MyClass (no attributes by default)."""
        self._inited = True

    def _year_limit(self, pub_year, yearGap = 2):
        current_year = datetime.now().year
        min_year = current_year - yearGap # Includes this year and previous 2 years by default
        return int(pub_year) >= min_year
            
        
    # (was) def fetch_publications_new_member(self, scholar_ids, domain):
    def fetch_crawler_publications(self, scholarLinks: list[str]) -> list[PublicationDTO]:
        """
        Fetches publications from Google Scholar for the given list of profile links.

        Args:
            scholarLinks (list): List of Google Scholar profile links.

        Returns:
            list[PublicationDTO]: List of publications found for the scholar links.
        """
        crawled: set[PublicationDTO] = set()
        for link in scholarLinks:
            scholar_id = self.extract_scholar_id(link)
            try:
                # Fetch author by scholar_id
                author_stub = scholarly.search_author_id(scholar_id)
                time.sleep(1)
                author = scholarly.fill(author_stub)
                time.sleep(5)
                author_name = author.get("name")
                for pub in author.get("publications"):
                    pub_title = pub.get("bib").get("title")
                    pub_year = pub.get("bib").get("pub_year")
                    author_pub_id = pub.get("author_pub_id")
                    if not pub_title or not pub_year:
                        print(f"GOOGLE CRAWLER => publication title or year found empty")
                        continue                
                    
                    # New publication -> create new pub
                    url = self.build_publication_url(scholar_id=scholar_id, author_pub_id=author_pub_id)
                    new_pub = PublicationDTO(
                        title= pub_title,
                        publication_year= pub_year,
                        publication_link= url,
                        authors= [author_name],
                        _scholarly_stub = pub
                    )
                    crawled.add(new_pub)
                    print(f"carwled {len(crawled)} publications so far")
            except Exception as e:
                print(f"[ERROR] Fetching publications for scholar_id {scholar_id}: {e}")
                continue
        return list(crawled)
    
    
    def fill_details(self, publicationDTOs: list[PublicationDTO]): #TODO: complete this function to also fill bibtex and arxiv, also think of how can we implement a queue of fill / crawl requests.
        """
        This method accepts a list of PublicationDTO where and fills description and authors into it
        """
        for pub in publicationDTOs:
            # stub = pub._scholarly_stub
            title = pub.title
            year = pub.publication_year
            author = pub.authors[0]
            query = f"{title} {author} {year}"
            # if not stub:
            #     continue
            try:
                # fetch full metadata for this stub
                # pub_obj = scholarly.search_single_pub(query) # HTML REQUEST
                # if not pub_obj:
                #     print(f"[WARN] No exact match found for pub: {title}")
                #     continue
                time.sleep(1)
                filled_pub = scholarly.fill(pub._scholarly_stub) #HTML REQUEST
                bib = filled_pub.get("bib") or {}
                # --authors--
                if "author" in bib:
                    authors_list = [a.strip() for a in bib.get("author").split(" and ")]
                    pub.set_authors(authors=authors_list)
                # --description--
                if "abstract" in bib:
                    pub.set_description(bib.get("abstract"))
                # --ArXiv/PDF link-- (if present)
                pub_url = filled_pub.get("pub_url") or bib.get("url")
                if pub_url and "arxiv.org" in pub_url:
                    pub.set_arxiv_link(pub_url)
                # --bibTex-- 
                bibtex_str = self.get_bibtex_from_citation_page(link=pub.publication_link) # no HTTP request
                if bibtex_str:
                    pub.set_bibtex(bibtex_str)
            except Exception as e:
                 print(f"[WARN] could not refill '{pub.title}': {e}")
                
    
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
    
    def normalize_title(self, title):
        title = title.lower()
        title = re.sub(r"[^a-z0-9]+", " ", title)
        return " ".join(title.split())

    def get_bibtex_from_citation_page(self, link: str) -> str | None:
        """
        Given a Google Scholar publication citation link, fetch the BibTeX citation using BeautifulSoup.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            # Step 1: Load the citation page
            response = requests.get(link, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # Step 2: Find the "Cite" (BibTeX) export link
            cite_link = soup.find("a", text="BibTeX")
            if not cite_link:
                # Try a more flexible search
                cite_link = soup.find("a", href=True, string=re.compile("BibTeX", re.IGNORECASE))

            if cite_link:
                bibtex_url = urljoin("https://scholar.google.com", cite_link["href"])
                time.sleep(1)  # politeness delay
                bib_response = requests.get(bibtex_url, headers=headers)
                bib_response.raise_for_status()
                return bib_response.text.strip()

            print(f"[WARN] BibTeX link not found on page: {link}")
            return None

        except Exception as e:
            print(f"[ERROR] Failed to fetch BibTeX from citation page: {e}")
            return None


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

