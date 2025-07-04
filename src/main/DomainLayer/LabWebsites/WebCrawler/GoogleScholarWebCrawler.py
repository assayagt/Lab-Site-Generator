import time
import re
from bs4 import BeautifulSoup 
from scholarly import scholarly
from urllib.parse import urlparse, parse_qs
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
                time.sleep(2)
                author = scholarly.fill(author_stub)
                time.sleep(3)
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
    
    
    def fill_details(self, publicationDTOs: list[PublicationDTO]): #TODO: complete this function to also fill bibtex and pub_url, also think of how can we implement a queue of fill / crawl requests.
        """
        This method accepts a list of PublicationDTO where and fills description and authors into it
        """
        for pub in publicationDTOs:
            try:
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
                pub_url = bib.get("url") or filled_pub.get("pub_url")
                if pub_url:
                    pub.set_pub_url(pub_url)
                # --bibTex-- 
                bibtex_str = self._construct_bibtex_from_filledPub(filled_pub)# no HTTP request
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
       
    def _construct_bibtex_from_filledPub(self, filled_pub):
        # ============ this part tries to avoid building the bibtex
        if 'bibtex' in filled_pub:
            return filled_pub['bibtex']
        bib = filled_pub.get('bib', {})
        if 'bibtex' in bib:
            return bib['bibtex']
        
        pub_url = filled_pub.get('pub_url', '')
        if 'scholar.bib' in pub_url:
            return self._fetch_bibtex_from_url(pub_url)
        # =============== up to here
        title = bib.get('title', 'Unknown Title')
        author = bib.get('author', 'Unknown Author')
        year = bib.get('pub_year', 'Unknown Year')
        venue = bib.get('venue', bib.get('journal', bib.get('booktitle', 'Unknown Venue')))
        # Generate a citation key
        first_author = author.split(' and ')[0]
        first_author_lastname = first_author.split()[-1].lower()
        citation_key = f"{first_author_lastname}{year}"
        citation_key = re.sub(r'[^a-zA-Z0-9]', '', citation_key) # remove special characters from citation key
        pub_type = self._determine_pub_type(bib, filled_pub)
        bibtex_lines = [f"@{pub_type}{{{citation_key},"]
        # Add fields
        if title:
            bibtex_lines.append(f'  title={{{title}}},')
        if author:
            bibtex_lines.append(f'  author={{{author}}},')
        if year and year != 'Unknown Year':
            bibtex_lines.append(f'  year={{{year}}},')
        # Add venue-specific fields
        if pub_type == 'article' and venue:
            bibtex_lines.append(f'  journal={{{venue}}},')
        elif pub_type == 'inproceedings' and venue:
            bibtex_lines.append(f'  booktitle={{{venue}}},')
        elif venue:
            bibtex_lines.append(f'  venue={{{venue}}},')
        # Add additional fields if available
        if 'volume' in bib:
            bibtex_lines.append(f'  volume={{{bib["volume"]}}},')
        if 'number' in bib:
            bibtex_lines.append(f'  number={{{bib["number"]}}},')
        if 'pages' in bib:
            bibtex_lines.append(f'  pages={{{bib["pages"]}}},')
        if 'publisher' in bib:
            bibtex_lines.append(f'  publisher={{{bib["publisher"]}}},')
        # Add URL if available
        if pub_url:
            bibtex_lines.append(f'  url={{{pub_url}}},')
        
        # Remove trailing comma from last entry and close
        if bibtex_lines[-1].endswith(','):
            bibtex_lines[-1] = bibtex_lines[-1][:-1]
        
        bibtex_lines.append('}')
        
        return '\n'.join(bibtex_lines)

    def _determine_pub_type(self, bib: dict, filled_pub: dict):
        """
        Determine the BibTeX publication type based on available metadata.
        """
        venue = bib.get('venue', '').lower()
        journal = bib.get('journal', '').lower()
        booktitle = bib.get('booktitle', '').lower()
        title = bib.get('title', '').lower()
        pub_url = filled_pub.get('pub_url', '')
        
        # Check for ArXiv papers first (high priority)
        if ('arxiv' in venue or 'arxiv' in pub_url.lower() or 
            'arxiv' in bib.get('eprint', '').lower()):
            return 'misc'
        
        # Check for other preprint servers
        preprint_servers = ['biorxiv', 'medrxiv', 'chemrxiv', 'preprints.org', 'ssrn']
        if any(server in pub_url.lower() for server in preprint_servers):
            return 'misc'
        
        # Check for thesis/dissertation
        thesis_keywords = ['thesis', 'dissertation', 'phd', 'master', 'msc', 'bachelor']
        if any(keyword in venue for keyword in thesis_keywords) or any(keyword in title for keyword in thesis_keywords):
            if 'phd' in venue or 'phd' in title or 'doctoral' in venue or 'doctoral' in title:
                return 'phdthesis'
            else:
                return 'mastersthesis'
        
        # Check for books
        book_keywords = ['book', 'handbook', 'manual', 'textbook']
        if any(keyword in venue for keyword in book_keywords):
            return 'book'
        
        # Check for book chapters
        chapter_keywords = ['chapter', 'book chapter']
        if any(keyword in venue for keyword in chapter_keywords):
            return 'incollection'
        
        # Check for conference proceedings/papers
        conference_keywords = ['conference', 'proceedings', 'workshop', 'symposium', 'meeting', 'summit', 'congress']
        if (any(keyword in venue for keyword in conference_keywords) or 
            any(keyword in booktitle for keyword in conference_keywords)):
            return 'inproceedings'
        
        # Check for unpublished works (before journal check)
        unpublished_keywords = ['unpublished', 'preprint', 'draft', 'submitted', 'under review']
        if any(keyword in venue for keyword in unpublished_keywords):
            return 'misc'  # Use misc instead of unpublished for preprints
        
        # Check for journal articles
        journal_keywords = ['journal', 'transactions', 'letters', 'review', 'magazine', 'quarterly', 'annual']
        if (any(keyword in venue for keyword in journal_keywords) or 
            journal or 'issn' in bib):
            return 'article'
        
        # Check for technical reports
        report_keywords = ['report', 'technical report', 'tech report', 'tr-', 'working paper']
        if any(keyword in venue for keyword in report_keywords):
            return 'techreport'
        
        # Check for online/web sources
        online_keywords = ['online', 'website', 'web', 'blog', 'url', 'http']
        if (any(keyword in venue for keyword in online_keywords) or 
            (pub_url and not any(ext in pub_url.lower() for ext in ['.pdf', '.ps', '.doc']))):
            return 'misc'
        
        # Check for patents
        if 'patent' in venue:
            return 'misc'  # BibTeX doesn't have a patent type, use misc
        
        # If we have a venue but can't classify it, default to misc
        if venue and venue != 'unknown venue':
            return 'misc'
        
        # Final fallback - if no clear venue info, use misc for safety
        return 'misc'
    
    def _fetch_bibtex_from_url(self, url: str):
        """
        Fetch BibTeX content from a URL (if scholarly provieds a direct BibTeX link)
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            content = response.text.strip()
            if content.startswith('@'):
                return content
        except Exception as e:
            print(f"[WARN] Could not fecth BibTeX fro URL {url}: {e}")
        return ""


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
        

