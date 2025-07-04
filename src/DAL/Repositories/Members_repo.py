class MembersRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def find_by_email(self, email: str):
        """
        Find all domains of some email
        """
        query = "SELECT domain FROM member_domain WHERE email = ?"
        result = self.db_manager.execute_query(query, (email,))
        if not result:
            return None
        return [row["domain"] for row in result]

    def find_by_domain(self, domain: str):
        """
        Find all emails that are incharge of some domain
        """
        query = "SELECT email FROM member_domain WHERE domain = ?"
        result = self.db_manager.execute_query(query, (domain,))
        if not result:
            return None
        return [row["email"] for row in result]

    def find_all(self):
        """
        Find all emails registered to the Generator system
        """
        query = "SELECT * FROM member_emails"
        result = self.db_manager.execute_query(query)
        return [row["email"] for row in result]

    def save_member(self, email):
        query = """
        INSERT INTO member_emails (email)
        VALUES (?)
        ON CONFLICT(email) DO NOTHING
        """
        rows_affected = self.db_manager.execute_update(query, (email,))
        return rows_affected > 0

    def save_domain(self, email, domain):
        query = """
        INSERT INTO member_domain (email, domain)
        VALUES (?, ?)
        ON CONFLICT (email, domain) DO NOTHING
        """
        rows_affected = self.db_manager.execute_update(query, (email, domain))
        return rows_affected > 0

    def delete_domain_from_user(self, email, domain):
        query = "DELETE FROM member_domain WHERE email = ? AND domain = ?"
        rows_affected = self.db_manager.execute_update(query, (email, domain))
        return rows_affected > 0

    def delete_domain(self, domain):
        query = "DELETE FROM member_domain WHERE domain = ?"
        rows_affected = self.db_manager.execute_update(query, (domain,))
        return rows_affected > 0

    def delete_member(self, email):
        query = "DELETE FROM members WHERE email = ?"
        rows_affected = self.db_manager.execute_update(query, (email,))
        return rows_affected > 0
