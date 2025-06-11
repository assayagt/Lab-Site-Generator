from src.DAL.DTOs.LabMember_dto import lab_member_dto

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
            domain, email, second_email, linkedin_link, scholar_link,
            media, full_name, degree, bio, profile_picture, email_notifications
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(domain, email) DO UPDATE SET
            second_email = excluded.second_email,
            linkedin_link = excluded.linkedin_link,
            scholar_link = excluded.scholar_link,
            media = excluded.media,
            full_name = excluded.full_name,
            degree = excluded.degree,
            bio = excluded.bio,
            profile_picture = excluded.profile_picture,
            email_notifications = excluded.email_notifications
        """
        params = (
            labMemberDTO.domain,
            labMemberDTO.email,
            labMemberDTO.second_email,
            labMemberDTO.linkedin_link,
            labMemberDTO.scholar_link,
            labMemberDTO.media,
            labMemberDTO.full_name,
            labMemberDTO.degree,
            labMemberDTO.bio,
            labMemberDTO.profile_picture,
            labMemberDTO.email_notifications
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

    def save_to_emails_pending(self, email, domain, status):
        query = """
        INSERT INTO emails_pending (domain, email, status)
        VALUES (?, ?, ?)
        ON CONFLICT(domain, email)
        DO UPDATE SET status = excluded.status
        """
        return self.db_manager.execute_update(query, (domain, email, status)) > 0
        
    
    def delete_LabMember(self, email, domain):
        query = "DELETE FROM lab_members WHERE email = ? AND domain = ?"
        return self.db_manager.execute_update(query, (email, domain)) > 0
    

    def _save_role(self, table, domain, email):
        self.clear_member_role(email=email, domain=domain)
        query = f"""
        INSERT INTO {table} (domain, email)
        VALUES (?, ?)
        ON CONFLICT(domain, email) DO NOTHING
        """
        return self.db_manager.execute_update(query, (domain, email)) > 0


    def _find_by_role(self, table, domain):
        query = f"""
            SELECT lm.* FROM lab_members AS lm
            INNER JOIN {table} AS role
            ON lm.domain = role.domain AND lm.email = role.email
            WHERE role.domain = ?
        """
        results = self.db_manager.execute_query(query, (domain,))
        return [self._row_to_labMember_dto(row) for row in results]
    
    def clear_member_role(self, email, domain):
        """
        Remove a (domain, email) pair from all LabRoles_* tables and emails_pending.
        """
        role_tables = [
            "LabRoles_users",
            "LabRoles_members",
            "LabRoles_managers",
            "LabRoles_siteCreator",
            "LabRoles_alumnis",
            "emails_pending"
        ]
        total_deleted = 0
        for table in role_tables:
            query = f"DELETE FROM {table} WHERE domain = ? AND email= ?"
            total_deleted += self.db_manager.execute_update(query, (domain, email))
        return total_deleted
    

    def _row_to_labMember_dto(self, row):
        return lab_member_dto(
            domain=row['domain'],
            email=row['email'],
            second_email=row['second_email'],
            linkedin_link=row['linkedin_link'],
            scholar_link=row['scholar_link'],
            media=row['media'],
            full_name=row['full_name'],
            degree=row['degree'],
            bio=row['bio'],
            profile_picture=row['profile_picture'],
            email_notifications=bool(row['email_notifications'])
        )
