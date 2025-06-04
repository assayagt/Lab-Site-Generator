import json
from src.main.DomainLayer.LabWebsites.Website.PublicationDTO import PublicationDTO
from src.main.DomainLayer.LabWebsites.Website.ApprovalStatus import ApprovalStatus
from src.main.DomainLayer.LabWebsites.WebCrawler.ScannedPublication import ScannedPublication

class PublicationRepository:
    """Handles databse operations for publications"""
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def find_by_id(self, paper_id):
        "Retrieve publication by ID"
        query = "SELECT * FROM publications WHERE paper_id = ?"
        result = self.db_manager.execute_query(query, (paper_id,))
        if not result:
            return None
        return self._row_to_publication_dto(result[0])
    
    def find_all(self):
        """
        Find all publications
            
        Returns:
            list: List of Publication_dto objects
        """
        query = "SELECT * FROM publications ORDER BY publication_year DESC, title ASC"
        results = self.db_manager.execute_query(query)
        return [self._row_to_publication_dto(row) for row in results]
    
    
    def find_by_domain(self, domain: str):
        """
        Retrive all publications of some domain.
        
        Args:
            domain(str): the domain to filter publicatios by.

        returns:
            List[Publication_dto]: A list of publications associated with the domain.
        """
        query="""
        SELECT *
        FROM publications
        WHERE publications.domain = ?
        ORDER BY publications.publication_year DESC, publications.title ASC
        """
        results = self.db_manager.execute_query(query, (domain,))
        return [self._row_to_publication_dto(row) for row in results]
    
    
    def save(self, publication_dto: PublicationDTO, domain: str):
        """
        Save a publication and link it to a domain using FK-safe upsert logic.
        """
        publication_query = """
        INSERT INTO publications (
            paper_id, title, authors, publication_year, approved,
            publication_link, video_link, git_link, presentation_link, description, author_emails, domain, scholarly_stub, bibtex, pub_url
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(paper_id) DO UPDATE SET
            title = excluded.title,
            authors = excluded.authors,
            publication_year = excluded.publication_year,
            approved = excluded.approved,
            publication_link = excluded.publication_link,
            video_link = excluded.video_link,
            git_link = excluded.git_link,
            presentation_link = excluded.presentation_link,
            description = excluded.description, 
            author_emails = excluded.author_emails,
            domain = excluded.domain,
            scholarly_stub = excluded.scholarly_stub,
            bibtex = excluded.bibtex,
            pub_url = excluded.pub_url
        """

        publication_parameters = (
            publication_dto.paper_id,
            publication_dto.title,
            json.dumps(publication_dto.authors or {}),
            publication_dto.publication_year,
            publication_dto.approved.value if publication_dto.approved else None,
            publication_dto.publication_link,
            publication_dto.video_link,
            publication_dto.git_link,
            publication_dto.presentation_link,
            publication_dto.description, 
            json.dumps(publication_dto.author_emails),
            publication_dto.domain,
            json.dumps(publication_dto._scholarly_stub or {}),
            publication_dto.bibtex,
            publication_dto.pub_url
        )

        try:
            self.db_manager.execute_update(publication_query, publication_parameters)
            return True
        except Exception as e:
            self.db_manager.logger.error(f"Failed to save publication: {e}")
            return False
        

    def delete(self, paper_id):
        """
        Delete a publication
        
        Args:
            paper_id (str): Publication ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        query = "DELETE FROM publications WHERE paper_id = ?"
        rows_affected = self.db_manager.execute_update(query, (paper_id,))
        return rows_affected > 0
    

    def _row_to_publication_dto(self, row):  
        return PublicationDTO(
            paper_id=row['paper_id'],
            title=row['title'],
            authors=json.loads(row['authors']),
            publication_year=row['publication_year'],
            approved=ApprovalStatus(row['approved']) if row['approved'] else None,
            publication_link=row['publication_link'],
            git_link=row['git_link'],
            video_link=row['video_link'],
            presentation_link=row['presentation_link'],
            description=row['description'],
            author_emails=json.loads(row['author_emails']),
            domain=row["domain"],
            _scholarly_stub=json.loads(row["scholarly_stub"] or "{}"),
            bibtex=row['bibtex'],
            pub_url=row['pub_url']
        )
    
    