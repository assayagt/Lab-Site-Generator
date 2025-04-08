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
        return self._row_to_labMember_dto(result[0]) if result else None

    def find_all_users_by_domain(self, domain):
        return self._find_by_role(table="LabRoles_users", domain=domain)


    def find_all_members_by_domain(self, domain):
        return self._find_by_role(table="LabRoles_members", domain=domain)

    def find_all_managers_by_domain(self, domain):
        return self._find_by_role(table="LabRoles_managers", domain=domain)

    def find_all_siteCreators_by_domain(self, domain):
        return self._find_by_role(table="LabRoles_siteCreator", domain=domain)

    def find_all_alumnis_by_domain(self, domain):
        return self._find_by_role(table="LabRoles_alumnis", domain=domain)

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
        query = """
        INSERT INTO lab_members (
            domain, email, second_email, linkedin_link,
            media, full_name, degree, bio
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(domain, email) DO UPDATE SET
            second_email = excluded.second_email,
            linkedin_link = excluded.linkedin_link,
            media = excluded.media,
            full_name = excluded.full_name,
            degree = excluded.degree,
            bio = excluded.bio
        """
        params = (
            labMemberDTO.domain,
            labMemberDTO.email,
            labMemberDTO.second_email,
            labMemberDTO.linkedin_link,
            labMemberDTO.media,
            labMemberDTO.full_name,
            labMemberDTO.degree,
            labMemberDTO.bio
        )
        return self.db_manager.execute_update(query, params) > 0
    

    def save_to_LabRoles_users(self, email, domain):
        return self._save_role(table="LabRoles_users", domain=domain, email=email)
    

    def save_to_LabRoles_members(self, email, domain):
        query="""
        INSERT OR REPLACE INTO LabRoles_members(domain, email)
        VALUES(?, ?)
        """
        return self._save_role(table="LabRoles_members", domain=domain, email=email)
    

    def save_to_LabRoles_managers(self, email, domain):
        return self._save_role(table="LabRoles_managers", domain=domain, email=email)
    

    def save_to_LabRoles_siteCreator(self, email, domain):
        return self._save_role(table="LabRoles_siteCreator", domain=domain, email=email)
    

    def save_to_LabRoles_alumnis(self, email, domain):
        return self._save_role(table="LabRoles_alumnis", domain=domain, email=email)
    

    def save_to_emails_pending(self, email, domain):
        query = """
        INSERT INTO emails_pending (domain, email)
        VALUES (?, ?)
        ON CONFLICT(domain, email) DO NOTHING
        """
        return self.db_manager.execute_update(query, (email, domain)) > 0
        
    
    def delete_LabMember(self, email, domain):
        query = "DELETE FROM lab_members WHERE email = ? AND domain = ?"
        return self.db_manager.execute_update(query, (email, domain)) > 0
    

    def _save_role(self, table, domain, email):
        query = f"""
        INSERT INTO {table} (domain, email)
        VALUES (?, ?)
        ON CONFLICT(domain, email) DO NOTHING
        """
        return self.db_manager.execute_update(query, (domain, email))


    def _find_by_role(self, table, domain):
        query = f"""
            SELECT lm.* FROM lab_members AS lm
            INNER JOIN {table} AS role
            ON lm.domain = role.domain AND lm.email = role.email
            WHERE role.domain = ?
        """
        results = self.db_manager.execute_query(query, (domain,))
        return [self._row_to_labMember_dto(row) for row in results]
    

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
