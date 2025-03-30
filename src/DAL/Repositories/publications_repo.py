from DTOs.Publication_dto import PublicationDTO


class PublicationRepository:
    """Handles databse operations for publications"""
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def find_by_id(self, paper_id):
        "Retrieve publication by ID"
        query = "SELECT * FROM publications WHERE paper_id = ?"
        result = self.db_manager.execute_query(query, (paper_id,))
        if not result: return None
        row = result[0]
        return PublicationDTO(
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
    
    def find_all(self):
        """
        Find all publications
            
        Returns:
            list: List of Publication objects
        """
        query = "SELECT * FROM publications ORDER BY publication_year DESC, title ASC"
        
        results = self.db_manager.execute_query(query)
        
        # Convert rows to Publication objects
        publications = []
        for row in results:
            publication = PublicationDTO(
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
            publications.append(publication)
        
        return publications
    
    def save(self, publication):
        """
        Save a publication (insert or update)
        
        Args:
            publication (Publication): Publication to save
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Check if the publication exists
        existing = self.find_by_id(publication.paper_id)
        
        if existing:
            # Update existing publication
            query = """
            UPDATE publications
            SET title = ?, authors = ?, publication_year = ?, approved = ?,
                publication_link = ?, video_link = ?, git_link = ?,
                presentation_link = ?, description = ?
            WHERE paper_id = ?
            """
            
            parameters = (
                publication.title,
                publication.authors,
                publication.publication_year,
                publication.approved,
                publication.publication_link,
                publication.video_link,
                publication.git_link,
                publication.presentation_link,
                publication.description,
                publication.paper_id
            )
        else:
            # Insert new publication
            query = """
            INSERT INTO publications
            (paper_id, title, authors, publication_year, approved,
             publication_link, video_link, git_link, presentation_link, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            parameters = (
                publication.paper_id,
                publication.title,
                publication.authors,
                publication.publication_year,
                publication.approved,
                publication.publication_link,
                publication.video_link,
                publication.git_link,
                publication.presentation_link,
                publication.description
            )
        
        rows_affected = self.db_manager.execute_update(query, parameters)
        return rows_affected > 0

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