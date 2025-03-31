from DTOs.SiteCustom_dto import SiteCustom_dto
import json

class SiteCustomsRepository:
    """Handles database operations for site customs"""
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def find_by_domain(self, domain):
        """retrieve siteCustom by domain"""
        query = "SELECT * FROM  site_customs WHERE domain = ?"
        result = self.db_manager.execute_query(query, (domain,))
        if not result: return None
        row = result[0]
        return SiteCustom_dto(
            domain=row['domain'],
            name=row['name'],
            components=json.loads(row['components']),
            template=row['template'],
            logo=row['logo'],
            home_picture=row['home_picture'],
            site_creator_email=row['creator_email'],
            generated=row['generated']
        )
    
    def find_all(self):
        """
        Find all site Customs in the database
        Returns list: List of siteCustom_dto objects
        """
        query = "SELECT * from site_customs"
        result = self.db_manager.execute_query(query)
        #Convert rows to siteCustom_dto objects
        siteCustoms = []
        for row in result:
            siteCustom = SiteCustom_dto(
                domain=row['domain'],
                name=row['name'],
                components_str=row['components'],
                template=row['template'],
                site_creator_email=row['creator_email'],
                logo=row['logo'],
                home_picture=row['home_pic'],
                generated=row['generated']
            )
    
    def save(self, siteCustom_dto: SiteCustom_dto):
        """This function gets a siteCustom and saves new or updates an existing site custom in the database"""
        existing = self.find_by_domain(siteCustom_dto.domain)
        if existing:
            # Update existing site_custom
            query = """
            UPDATE site_customs
            SET name = ?, components = ?, template = ?, creator_email = ?,
                logo = ?, nome_pic = ?, generated = ?
            WHERE domain = ?
            """
            parameters = (
                siteCustom_dto.name,
                siteCustom_dto.components_str,
                siteCustom_dto.template,
                siteCustom_dto.site_creator_email,
                siteCustom_dto.logo,
                siteCustom_dto.home_picture,
                siteCustom_dto.generated
            )
        else:
            # Insert new siteCustom
            query = """
            INSERT INTO site_customs
            (domain, name, components, template, creator_email,
             logo, home_pic, generated)
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
