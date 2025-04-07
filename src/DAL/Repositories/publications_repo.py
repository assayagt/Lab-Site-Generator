from DTOs.Publication_dto import Publication_dto


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

    
    
    def save(self, publication_dto: Publication_dto, domain: str):
        """
        Save a publication and link it to a domain (insert or update)
        
        Args:
            publication (Publication): Publication to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        publication_query = """
        INSERT OR REPLACE INTO publications (
            paper_id, title, authors, publication_year, approved,
            publication_link, video_link, git_link, presentation_link, description
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        publication_parameters = (
            publication_dto.paper_id,
            publication_dto.title,
            publication_dto.authors,
            publication_dto.publication_year,
            publication_dto.approved,
            publication_dto.publication_link,
            publication_dto.video_link,
            publication_dto.git_link,
            publication_dto.presentation_link,
            publication_dto.description
        )

        link_query = """
        INSERT OR IGNORE INTO domain_paperID (domain, paper_id)
        VALUES (?, ?)
        """
        link_parameters = (domain, publication_dto.paper_id)
        # Execute both queries in a single transaction
        try:
            with self.db_manager.lock:
                self.db_manager.execute_update(publication_query, publication_parameters)
                self.db_manager.execute_update(link_query, link_parameters)
            return True
        except Exception as e:
            self.db_manager.logger.error(f"Failed to save publication: {e}")
            return False

    def delete_publication(self, paper_id):
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
        return Publication_dto(
            paper_id=row['paper_id'],
                title=row['title'],
                authors=row['authors'],
                publication_year=row['publication_year'],
                approved=row['approved'],
                publication_link=row['publication_link'],
                git_link=row['git_link'],
                video_link=row['video_link'],
                presentation_link=row['presentation_link'],
                description=row['description']
            )