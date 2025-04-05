from DTOs.Member_dto import member_dto

class WebsiteRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager


    def find_by_email(self, email: str):
        pass

    def find_all(self):
        pass
    
    def save(self, member_dto: member_dto):
        pass
    