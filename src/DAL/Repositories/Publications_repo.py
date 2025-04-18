# import sys
# import os


# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
# if project_root not in sys.path:
#     sys.path.append(project_root)
import json
from src.main.DomainLayer.LabWebsites.Website.PublicationDTO import PublicationDTO
from src.main.DomainLayer.LabWebsites.Website.ApprovalStatus import ApprovalStatus

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
        SELECT p.*
        FROM publications p
        INNER JOIN domain_paperID d ON p.paper_id = d.paper_id
        WHERE d.domain = ?
        ORDER BY p.publication_year DESC, p.title ASC
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
            publication_link, video_link, git_link, presentation_link, description, author_emails
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            author_emails = excluded.author_emails
        """
        approved = publication_dto.approved.value if approved else None

        publication_parameters = (
            publication_dto.paper_id,
            publication_dto.title,
            json.dumps(publication_dto.authors),
            publication_dto.publication_year,
            approved,
            publication_dto.publication_link,
            publication_dto.video_link,
            publication_dto.git_link,
            publication_dto.presentation_link,
            publication_dto.description, 
            json.dumps(publication_dto.author_emails)
        )

        link_query = """
        INSERT INTO domain_paperID (domain, paper_id)
        VALUES (?, ?)
        ON CONFLICT(domain, paper_id) DO NOTHING
        """
        link_parameters = (domain, publication_dto.paper_id)

        try:
            self.db_manager.execute_update(publication_query, publication_parameters)
            self.db_manager.execute_update(link_query, link_parameters)
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
                author_emails=json.loads(row['author_emails'])
            )