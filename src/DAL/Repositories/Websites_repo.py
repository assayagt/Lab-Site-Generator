from src.DAL.DTOs.Website_dto import website_dto
from src.DAL.database_manager import DatabaseManager
class WebsiteRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def find_by_domain(self, domain):
        query = "SELECT * FROM websites WHERE domain = ?"
        result = self.db_manager.execute_query(query, (domain,))
        if not result:
            return None
        return self._row_to_website_dto(row=result[0])

    def find_all(self):
        query = "SELECT * FROM websites"
        results = self.db_manager.execute_query(query)
        return [self._row_to_website_dto(row) for row in results] if results else []
    
    def find_all_domains(self) -> list[str]:
        query = "SELECT domain FROM websites"
        results = self.db_manager.execute_query(query)
        return [row['domain'] for row in results] if results else []
        

    def save(self, website_dto: website_dto):
        """
        Save a website entry. Updates if domain exists, otherwise inserts.
        Args:
            website_dto (WebsiteDTO): The website data transfer object.
            user_email (str, optional): The email of the user creating the website.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """       
        # Use INSERT OR REPLACE to update or insert
        query = """
        INSERT INTO websites
        (domain, contact_info, about_us)
        VALUES (?, ?, ?)
        ON CONFLICT(domain) DO UPDATE SET
            contact_info = excluded.contact_info,
            about_us = excluded.about_us
        """
        parameters = (
            website_dto.domain,
            website_dto.contact_info,
            website_dto.about_us
        )
        return(self.db_manager.execute_update(query, parameters) > 0 )

        

    def delete_website(self, domain):
        """
        Delete a website
        
        Args:
            domain (str): website's domain
            
        Returns:
            bool: True if successful, False otherwise
        """
        query = "DELETE FROM websites WHERE domain = ?"
        rows_affected = self.db_manager.execute_update(query, (domain,))
        return rows_affected > 0
    
    def _row_to_website_dto(self, row):
        return website_dto(
            domain=row['domain'],
            contact_info=row['contact_info'],
            about_us=row['about_us']
        )
