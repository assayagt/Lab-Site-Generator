import threading

from src.DAL.Repositories.Members_repo import MembersRepository
from src.DAL.Repositories.LabMembers_repo import LabMembersRepository
from src.DAL.Repositories.Notifications_repo import NotificationRepository
from src.DAL.Repositories.Publications_repo import PublicationRepository
from src.DAL.Repositories.SiteCustoms_repo import SiteCustomsRepository
from src.DAL.Repositories.Websites_repo import WebsiteRepository
from src.DAL.database_manager import DatabaseManager
from  src.DAL.Repositories.News_repo import News_repo

class DAL_controller:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, db_manager=None):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_manager=None):
        if getattr(self, "_inited", False):
            return

        self._db_manager = db_manager or DatabaseManager()
        self.members_repo = MembersRepository(db_manager=self._db_manager)
        self.publications_repo = PublicationRepository(db_manager=self._db_manager)
        self.siteCustom_repo = SiteCustomsRepository(db_manager=self._db_manager)
        self.website_repo = WebsiteRepository(db_manager=self._db_manager)
        self.notifications_repo = NotificationRepository(db_manager=self._db_manager)
        self.LabMembers_repo = LabMembersRepository(db_manager=self._db_manager)
        self.News_repo = News_repo(db_manager=self._db_manager)
        self._initialized = True

    @classmethod
    def reset_instance(cls):
        """Reset the singleton instance. Safe to use in unit tests."""
        with cls._lock:
            cls._instance = None

    def drop_all_tables(self):
        self._db_manager.clear_all_tables()

    