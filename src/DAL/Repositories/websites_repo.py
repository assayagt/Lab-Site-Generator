from DTOs.website_dto import Website_dto

class WebsiteRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def find_by_domain(self, domain):
        query = "SELECT * FROM websites WHERE domain = ?"
        result = self.db_manager.execute_query(query, (domain,))
        if not result: return None
        row = result[0]
        return Website_dto(
            domain=row['domain'],
            contact_info=row['contact_info'],
            about_us=row['about_us']
        )
    
    def save(self, website_dto: Website_dto):
        # Check if the website exists
        existing = self.find_by_domain(website_dto.domain)
        if existing:
            # Update exsisting website
            query = """
            UPDATE websites
            SET contact_info = ?, about_us = ?
            WHERE domain = ?
            """
            parameters = (
                website_dto.contact_info,
                website_dto.about_us
            )
        else:
            query = """
            INSERT INTO websites
            (domain, contact_info, about_us)
            VALUES (?, ?, ?)
            """
            parameters = (
                website_dto.domain,
                website_dto.contact_info,
                website_dto.about_us
            )
        rows_affected = self.db_manager.exectute_update(query, parameters)
        return rows_affected > 0
