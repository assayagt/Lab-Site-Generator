from DTOs.Website_dto import website_dto

class WebsiteRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def find_by_domain(self, domain):
        query = "SELECT * FROM websites WHERE domain = ?"
        result = self.db_manager.execute_query(query, (domain,))
        if not result:
            return None
        row = result[0]
        return website_dto(
            domain=row['domain'],
            contact_info=row['contact_info'],
            about_us=row['about_us']
        )
    
    def find_by_email(self, email):
        query = """
        SELECT w.domain, w.contact_info, w.about_us
        FROM member_domain m
        JOIN websites w ON m.domain = w.domain
        WHERE m.email = ?
        """
        result = self.db_manager.execute_query(query, (email,))
        if not result:
            return None

        websites = []
        for row in result:
            website = website_dto(
                domain=row['domain'],
                contact_info=row['contact_info'],
                about_us=row['about_us']
            )
            websites.append(website)
        return websites


    def save(self, website_dto: website_dto, user_email: str = None):
        """
        Save a website entry. If it exists, it is replaced. Otherwise, a new entry is inserted.

        Args:
            website_dto (WebsiteDTO): The website data transfer object.
            user_email (str, optional): The email of the user creating the website.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        if user_email is None:
            raise ValueError("User email is required when inserting a new website.")

        
        conn = self.db_manager.connect()
        cursor = conn.cursor()

        # Use INSERT OR REPLACE to update or insert
        query = """
        INSERT OR REPLACE INTO websites
        (domain, contact_info, about_us)
        VALUES (?, ?, ?)
        """
        parameters = (
            website_dto.domain,
            website_dto.contact_info,
            website_dto.about_us
        )
        self.db_manager.execute_update(query, parameters)

        # Ensure membership exists in member_domain (INSERT OR IGNORE prevents duplicates)
        query2 = """
        INSERT OR IGNORE INTO member_domain
        (email, domain)
        VALUES(?, ?)
        """
        parameters2 = (user_email, website_dto.domain)
        self.db_manager.execute_update(query2, parameters2)

        conn.commit()  # Commit both operations atomically
        return cursor.rowcount > 0  # Returns True if any rows were affected
        
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

