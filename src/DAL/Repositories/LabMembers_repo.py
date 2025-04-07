from DTOs.LabMember_dto import lab_member_dto

class LabMembersRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def find_LabMember_by_domain_email(self, domain, email):
        query="""
        SELECT * FROM lab_members
        WHERE domain = ? AND email = ?
        """
        result = self.db_manager.execute_query(query, (domain, email))
        return self._row_to_labMember_dto(result[0])

    def find_all_users_by_domain(self, domain):
        query="""
        SELECT lm.*
        FROM lab_members AS lm
        INNER JOIN LabRoles_users AS lru
        ON lm.domain = lru.domain AND lm.email = lru.email
        WHERE lru.domain = ?;
        """
        results = self.db_manager.execute_query(query, (domain,))
        return [self._row_to_labMember_dto(row) for row in results]


    def find_all_members_by_domain(self, domain):
        query="""
        SELECT lm.*
        FROM lab_members AS lm
        INNER JOIN LabRoles_members AS lrm
        ON lm.domain = lrm.domain AND lm.email = lrm.email
        WHERE lrm.domain = ?;
        """
        results = self.db_manager.execute_query(query, (domain,))
        return [self._row_to_labMember_dto(row) for row in results]

    def find_all_managers_by_domain(self, domain):
        query="""
        SELECT lm.*
        FROM lab_members AS lm
        INNER JOIN LabRoles_managers AS lrm
        ON lm.domain = lrm.domain AND lm.email = lrm.email
        WHERE lrm.domain = ?;
        """
        results = self.db_manager.execute_query(query, (domain,))
        return [self._row_to_labMember_dto(row) for row in results]

    def find_all_siteCreators_by_domain(self, domain):
        query="""
        SELECT lm.*
        FROM lab_members AS lm
        INNER JOIN LabRoles_siteCreator AS lrs
        ON lm.domain = lrs.domain AND lm.email = lrs.email
        WHERE lrs.domain = ?;
        """
        results = self.db_manager.execute_query(query, (domain,))
        return [self._row_to_labMember_dto(row) for row in results]

    def find_all_alumnis_by_domain(self, domain):
        query="""
        SELECT lm.*
        FROM lab_members AS lm
        INNER JOIN LabRoles_users AS lra
        ON lm.domain = lra.domain AND lm.email = lra.email
        WHERE lra.domain = ?;
        """
        results = self.db_manager.execute_query(query, (domain,))
        return [self._row_to_labMember_dto(row) for row in results]

    def find_all_pending_emails_by_domain(self, domain):
        query="""
        SELECT email
        FROM emails_pending
        WHERE domain = ?;
        """
        results = self.db_manager.execute_query(query, (domain,))
        return [row['email'] for row in results]


    #==========SAVE SECTION -> Later for easier data handling we can keep only the save_to_labRoles functions and merge them with save_labMember function
    # we can do that by deleting the labMember (and so it will be deleted from whatever role it has and then insert it again to the table along with the proper role)
    def save_LabMember(self, labMemberDTO: lab_member_dto):
        """This function gets a lab member and saves or updates it in the database"""
        query="""
        INSERT OR REPLACE INTO lab_members(
        domain, email, second_email, linkedin_link, media, full_name, degree, bio
        )
        VALUES(?, ?, ?, ?, ?, ?, ?, ?)
        """
        params=(
            labMemberDTO.domain,
            labMemberDTO.email,
            labMemberDTO.second_email,
            labMemberDTO.linkedin_link,
            labMemberDTO.media,
            labMemberDTO.full_name,
            labMemberDTO.degree,
            labMemberDTO.bio
        )
        rows_affected = self.db_manager.execute_update(query, params)
        return rows_affected > 0
    

    def save_to_LabRoles_users(self, email, domain):
        query="""
        INSERT OR REPLACE INTO LabRoles_users(domain, email)
        VALUES(?, ?)
        """
        params=(domain, email)
        rows_affected = self.db_manager.execute_update(query, params)
        return rows_affected > 0
    

    def save_to_LabRoles_members(self, email, domain):
        query="""
        INSERT OR REPLACE INTO LabRoles_members(domain, email)
        VALUES(?, ?)
        """
        params=(domain, email)
        rows_affected = self.db_manager.execute_update(query, params)
        return rows_affected > 0
    

    def save_to_LabRoles_managers(self, email, domain):
        query="""
        INSERT OR REPLACE INTO LabRoles_managers(domain, email)
        VALUES(?, ?)
        """
        params=(domain, email)
        rows_affected = self.db_manager.execute_update(query, params)
        return rows_affected > 0
    

    def save_to_LabRoles_siteCreator(self, email, domain):
        query="""
        INSERT OR REPLACE INTO LabRoles_siteCreator(domain, email)
        VALUES(?, ?)
        """
        params=(domain, email)
        rows_affected = self.db_manager.execute_update(query, params)
        return rows_affected > 0
    

    def save_to_LabRoles_alumnis(self, email, domain):
        query="""
        INSERT OR REPLACE INTO LabRoles_alumnis(domain, email)
        VALUES(?, ?)
        """
        params=(domain, email)
        rows_affected = self.db_manager.execute_update(query, params)
        return rows_affected > 0
    

    def save_to_emails_pending(self, email, domain):
        query="""
        INSERT OR REPLACE INTO emails_pending(domain, email)
        VALUES(?, ?)
        """
        params=(domain, email)
        rows_affected = self.db_manager.execute_update(query, params)
        return rows_affected > 0
    
    def delete_LabMember(self, email, domain):
        query = "DELETE FROM lab_members WHERE email = ? AND domain = ?"
        rows_affected = self.db_manager.execute_update(query, (email, domain))
        return rows_affected > 0
    

    def _row_to_labMember_dto(self, row):
        return lab_member_dto(
            domain=row['domain'],
            email=row['email'],
            second_email=row['second_email'],
            linkedin_link=row['linkedin_link'],
            media=row['media'],
            full_name=row['full_name'],
            degree=row['degree'],
            bio=row['bio']
        )
