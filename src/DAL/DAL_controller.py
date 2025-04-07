from Repositories.Members_repo import MembersRepository
from Repositories.LabMembers_repo import LabMembersRepository
from Repositories.Notifications_repo import NotificationRepository
from Repositories.Publications_repo import PublicationRepository
from Repositories.SiteCustoms_repo import SiteCustomsRepository
from Repositories.Websites_repo import WebsiteRepository
from database_manager import DatabaseManager

class DAL_controller:

    _instance = None  # Class-level reference to the singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DAL_controller, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return  # Avoid re-initializing on subsequent instantiations

        self._db_manager = DatabaseManager()
        self.members_repo = MembersRepository(db_manager=self._db_manager)
        self.publications_repo = PublicationRepository(db_manager=self._db_manager)
        self.siteCustom_repo = SiteCustomsRepository(db_manager=self._db_manager)
        self.website_repo = WebsiteRepository(db_manager=self._db_manager)
        self.notifications_repo = NotificationRepository(db_manager=self._db_manager)
        self.LabMembers_repo = LabMembersRepository(db_manager=self._db_manager)
        self._initialized = True

    