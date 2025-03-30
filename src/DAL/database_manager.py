import sqlite3
import os
import logging

class DatabaseManager:
    def __init__(self, db_path='LSG.db'):
        """
        Initialize the database manager
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.logger = logging.getLogger(__name__)
        self.db_path = os.path.abspath(db_path)
        
        #Ensure database directory exists
        os.makedirs(os.path.dirname(self.db_path) or '.', exist_ok=True)
        #Initialize connection
        self.connection = None
        
        self.logger.info(f"Database manager initialized with database at {self.db_path}")
    
    def connect(self):
        """Create and return a database connection"""
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
        return self.connection
    
    def get_cursor(self):
        """Get a database cursor"""
        conn = self.connect()
        return conn.cursor()
    
    def execute_query(self, query, parameters=None):
        """
        Execute a SQL query and return the results

        Args:
            query (str): SQL query to execute
            parameters (tuple): parameters for the query
        Returns:
            list: Query results
        """
        cursor = self.get_cursor()
        try:
            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)
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
        cursor = self.get_cursor()
        try:
            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)
            
            self.connection.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            self.connection.rollback()
            self.logger.error(f"Database error: {e}")
            raise

    def execute_script(self, script):
        """
        Execute a SQL script
        
        Args:
            script (str): SQL script to execute
        """
        conn = self.connect()
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