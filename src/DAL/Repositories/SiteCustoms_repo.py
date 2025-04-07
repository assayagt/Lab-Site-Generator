from DTOs.SiteCustom_dto import siteCustom_dto
import json

class SiteCustomsRepository:
    """Handles database operations for site customs"""
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def find_by_domain(self, domain):
        """retrieve siteCustom by domain"""
        query = "SELECT * FROM  site_customs WHERE domain = ?"
        result = self.db_manager.execute_query(query, (domain,))
        if not result:
            return None
        return self._row_to_SiteCustom_dto(result[0])
    
    def find_all(self):
        """
        Find all site Customs in the database
        Returns list: List of siteCustom_dto objects
        """
        query = "SELECT * from site_customs"
        results = self.db_manager.execute_query(query)
        #Convert rows to siteCustom_dto objects
        return [self._row_to_SiteCustom_dto(row) for row in results]
    
    def find_by_email(self, email: str): #TODO: implement this method later
        pass
    
    def save(self, siteCustom_dto: siteCustom_dto):
        """This function gets a siteCustom and saves or updates a site custom in the database"""
        query = """
        INSERT OR REPLACE INTO site_customs (
            domain, name, components, template, creator_email,
            logo, home_pic, generated
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        parameters = (
            siteCustom_dto.domain,
            siteCustom_dto.name,
            siteCustom_dto.components_str,
            siteCustom_dto.template,
            siteCustom_dto.site_creator_email,
            siteCustom_dto.logo,
            siteCustom_dto.home_picture,
            siteCustom_dto.generated
        )
        rows_affected = self.db_manager.execute_update(query, parameters)
        return rows_affected > 0
    
    def delete(self, domain):
        query = "DELETE FROM publications WHERE domain = ?"
        rows_affected = self.db_manager.execute_update(query, (domain,))
        return rows_affected > 0


    def _row_to_SiteCustom_dto(self, row):
        return siteCustom_dto(
            domain=row['domain'],
            name=row['name'],
            components_str=row['components'],
            template=row['template'],
            logo=row['logo'],
            home_picture=row['home_pic'],
            site_creator_email=row['creator_email'],
            generated=bool(row['generated'])
        ) 