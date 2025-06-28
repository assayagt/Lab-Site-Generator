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

    def find_all_lab_members_by_domain(self, domain):
        return self._find_by_role(role="member", domain=domain)

    def find_all_managers_by_domain(self, domain):
        return self._find_by_role(role="manager", domain=domain)

    def find_all_siteCreators_by_domain(self, domain):
        return self._find_by_role(role="creator", domain=domain)

    def find_all_alumnis_by_domain(self, domain):
        return self._find_by_role(role="alumni", domain=domain)

    def find_all_by_domain(self, domain):
        # get all members from lab_members table by the domain
        query = """
        SELECT * FROM lab_members
        WHERE domain = ?
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
    
    #get status of email by domain and email
    def get_status_of_email_by_domain_email(self, domain, email):
        query = """
        SELECT status FROM emails_pending WHERE domain = ? AND email = ?
        """
        result = self.db_manager.execute_query(query, (domain, email))
        return result[0]['status'] if result else None


    #==========SAVE SECTION -> Later for easier data handling we can keep only the save_to_labRoles functions and merge them with save_labMember function
    # we can do that by deleting the labMember (and so it will be deleted from whatever role it has and then insert it again to the table along with the proper role)
    def save_LabMember(self, labMemberDTO: lab_member_dto):
        query = """
        INSERT INTO lab_members (
            domain, email, second_email, linkedin_link, scholar_link,
            media, full_name, degree, bio, profile_picture, email_notifications, role
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(domain, email) DO UPDATE SET
            second_email = excluded.second_email,
            linkedin_link = excluded.linkedin_link,
            scholar_link = excluded.scholar_link,
            media = excluded.media,
            full_name = excluded.full_name,
            degree = excluded.degree,
            bio = excluded.bio,
            profile_picture = excluded.profile_picture,
            email_notifications = excluded.email_notifications,
            role = excluded.role
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
            labMemberDTO.email_notifications,
            labMemberDTO.role
        )
        return self.db_manager.execute_update(query, params) > 0
    
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
    
    def delete_from_emails_pending(self, email, domain):
        query = "DELETE FROM emails_pending WHERE email = ? AND domain = ?"
        return self.db_manager.execute_update(query, (email, domain)) > 0

    def _find_by_role(self, role, domain):
        query = """
        SELECT * FROM lab_members
        WHERE domain = ? AND role = ?
        """
        result = self.db_manager.execute_query(query, (domain, role))
        return [self._row_to_labMember_dto(row) for row in result]

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
            email_notifications=bool(row['email_notifications']),
            role=row['role']
        )
