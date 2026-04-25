"""
Database utilities for MongoDB connection
For prototype: This is optional and not yet implemented
"""

from pymongo import MongoClient
from config import Config

class Database:
    """MongoDB database connection handler"""
    
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def connect(self):
        """Establish connection to MongoDB"""
        if self._client is None:
            try:
                self._client = MongoClient(Config.MONGODB_URI)
                self._db = self._client[Config.MONGODB_DB]
                print(f"Connected to MongoDB: {Config.MONGODB_DB}")
            except Exception as e:
                print(f"Failed to connect to MongoDB: {e}")
                raise
    
    def get_db(self):
        """Get database instance"""
        if self._db is None:
            self.connect()
        return self._db
    
    def close(self):
        """Close database connection"""
        if self._client is not None:
            self._client.close()
            self._client = None
            self._db = None


# Singleton instance
db = Database()

