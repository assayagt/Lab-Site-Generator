import sqlite3
import os
import logging
import threading

class DatabaseManager:

    _instance = None
    _instance_lock = threading.Lock() # Ensures singleton creation is thread-safe
    
    def __new__(cls, db_path='LSG.db'):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super(DatabaseManager, cls).__new__(cls)
                # Initialize instance attributes
                cls._instance.db_path = os.path.abspath(db_path)
                os.makedirs(os.path.dirname(cls._instance.db_path) or '.', exist_ok=True)
                cls._instance.connection = None
                cls._instance.lock = threading.Lock() # Lock for concurrent DB operations
                cls._instance.logger =logging.getLogger(__name__)
                cls._instance.logger.info(f"Database manager initialized with database at {cls._instance.db_path}")
            return cls._instance



    # def __init__(self, db_path='LSG.db'):
    #     """
    #     Initialize the database manager
        
    #     Args:
    #         db_path (str): Path to the SQLite database file
    #     """
    #     self.logger = logging.getLogger(__name__)
    #     self.db_path = os.path.abspath(db_path)
        
    #     #Ensure database directory exists
    #     os.makedirs(os.path.dirname(self.db_path) or '.', exist_ok=True)
    #     #Initialize connection
    #     self.connection = None
        
    #     self.logger.info(f"Database manager initialized with database at {self.db_path}")
    
    def connect(self):
        """Create and return a database connection.
            Use check_same_thread=False to allow usage accross threads."""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def get_cursor(self):
        """Get a database cursor"""
        conn = self.connect()
        return conn.cursor()
    
    def execute_query(self, query, parameters=None):
        """
        Execute a SQL query and return the results
        Uses an instance lock to ensure that concurrent access to the DB connection is synchronized.

        Args:
            query (str): SQL query to execute
            parameters (tuple): parameters for the query
        Returns:
            list: Query results
        """
        conn = self.connect() # Ensure there is an active connection to narrow thread bottleneck.
        with self.lock: # Synchronize database access
            cursor = self.get_cursor()
            try:
                if parameters:
                    cursor.execute(query, parameters)
                else:
                    cursor.execute(query)
                conn.commit()
                return cursor.fetchall()
            except sqlite3.Error as e:
                self.logger.error(f"Database error: {e}")
                raise

    def execute_update(self, query, parameters=None):
        """
        Execute a SQL update query
        
        Args:
            query (str): SQL query to execute
            parameters (tuple): Parameters for the query
        Returns:
            int: Number of rows affected
        """
        conn = self.connect()
        with self.lock:    
            cursor = self.get_cursor()
            try:
                if parameters:
                    cursor.execute(query, parameters)
                else:
                    cursor.execute(query)
                
                conn.commit()
                return cursor.rowcount
            except sqlite3.Error as e:
                conn.rollback()
                self.logger.error(f"Database error: {e}")
                raise

    def execute_script(self, script):
        """
        Execute a SQL script
        
        Args:
            script (str): SQL script to execute
        """
        conn = self.connect()
        with self.lock:
            try:
                conn.executescript(script)
                conn.commit()
                self.logger.info("SQL script executed successfully")
            except sqlite3.Error as e:
                conn.rollback()
                self.logger.error(f"Database error: {e}")
                raise

    def create_tables(self):
        """Create database tables if they don't exist"""
        self.execute_script('PRAGMA foreign_keys = ON;') # Enable foreign keys in SQLite
        
        publications_table = '''
        CREATE TABLE IF NOT EXISTS publications (
            paper_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            authors TEXT NOT NULL,
            publication_year INTEGER,
            approved TEXT,
            publication_link TEXT,
            video_link TEXT,
            git_link TEXT,
            presentation_link TEXT,
            description TEXT
        );
        '''
        self.execute_script(publications_table)

        domain_paperID_table = '''
        CREATE TABLE IF NOT EXISTS domain_paperID(
            domain TEXT,
            paper_id TEXT,
            FOREIGN KEY (domain) REFERECES websites(domain) ON DELETE CASCADE,
            FOREIGN KEY (paper_id) REFERENCES publicatios(paper_id) ON DELETE CASCADE
        );
        '''
        self.execute_script(domain_paperID_table)
        

        member_domain_table = '''
        CREATE TABLE IF NOT EXISTS member_domain(
        email TEXT,
        domain TEXT,
        PRIMARY KEY (email, domain),
        FOREIGN KEY (domain) REFERENCES websites(domain) ON DELETE CASCADE
        );
        '''
        self.execute_script(member_domain_table)
        
        SiteCustoms_table = '''
        CREATE TABLE IF NOT EXISTS site_customs(
            domain TEXT PRIMARY KEY,
            name TEXT,
            creator_email TEXT,
            components TEXT,
            template TEXT,
            logo BLOB,
            home_pic BLOB,
            generated INTEGER
            FOREIGN KEY (domain) REFERENCES websites(domain) ON DELETE CASCADE
        );
        '''
        self.execute_script(SiteCustoms_table)

        Websites_table = '''
        CREATE TABLE IF NOT EXISTS websites(
            domain TEXT PRIMARY KEY,
            contact_info TEXT,
            about_us TEXT
        );
        '''
        self.execute_script(Websites_table)

        self.logger.info("Database tables created successfully")

    def close(self):
        """Close the database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.logger.info("Database connection closed")

    def __del__(self):
        """Ensure connection is closed when the object is deleted"""
        self.close()