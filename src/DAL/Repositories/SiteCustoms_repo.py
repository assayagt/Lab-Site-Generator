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
    
    def find_by_email(self, email: str):
        query = """
        SELECT sc.*
        FROM member_domain m
        JOIN site_Customs sc ON m.domain = sc.domain
        WHERE m.email = ?
        """
        result = self.db_manager.execute_query(query, (email,))
        if not result:
            return None
        return [self._row_to_SiteCustom_dto(row) for row in result]
    
    def save(self, siteCustom_dto: siteCustom_dto, user_email=None):
        """This function gets a siteCustom and saves or updates a site custom in the database"""

        query = """
        INSERT INTO site_customs (
            domain, name, components, template, creator_email,
            logo, home_pic, generated
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(domain) DO UPDATE SET
            name = excluded.name,
            components = excluded.components,
            template = excluded.template,
            creator_email = excluded.creator_email,
            logo = excluded.logo,
            home_pic = excluded.home_pic,
            generated =excluded.generated
        """
        parameters = (
            siteCustom_dto.domain,
            siteCustom_dto.name,
            siteCustom_dto.components_str,
            siteCustom_dto.template,
            siteCustom_dto.site_creator_email,
            siteCustom_dto.logo,
            siteCustom_dto.home_picture,
            int(siteCustom_dto.generated)
        )

        # Ensure membership exists in member_domain (INSERT OR IGNORE prevents duplicates)
        query2 = """
        INSERT INTO member_domain
        (email, domain)
        VALUES(?, ?)
        ON CONFLICT(email, domain) DO NOTHING
        """
        parameters2 = (user_email, siteCustom_dto.domain)
        try:
            self.db_manager.execute_update(query, parameters)
            if user_email is not None:
                self.db_manager.execute_update(query2, parameters2)
            return True
        except Exception as e:
            self.db_manager.logger.error(f"Failed to save publication: {e}")
            return False
    
    def delete(self, domain):
        query = "DELETE FROM site_customs WHERE domain = ?"
        rows_affected = self.db_manager.execute_update(query, (domain,))
        return rows_affected > 0
    
    def delete_website_from_member(self, domain, email):
        query = "DELETE FROM member_domain WHERE email = ? AND domain = ?"
        rows_affecterd = self.db_manager.execute_update(query, (email, domain))
        return rows_affecterd > 0


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