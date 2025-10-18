import sqlite3
import os
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """Singleton database connection manager for SQLite"""
    
    _instance: Optional['DatabaseConnection'] = None
    _connection: Optional[sqlite3.Connection] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection, creating it if it doesn't exist"""
        if self._connection is None:
            # Get database path from config
            db_path = Path(__file__).parent.parent / "cards.db"
            
            logger.info(f"Connecting to database: {db_path}")
            self._connection = sqlite3.connect(str(db_path))
            self._connection.row_factory = sqlite3.Row  # Enable dict-like access
            
            # Enable foreign keys
            self._connection.execute("PRAGMA foreign_keys = ON")
            
        return self._connection
    
    def close_connection(self):
        """Close database connection"""
        if self._connection:
            self._connection.close()
            self._connection = None
            logger.info("Database connection closed")
    
    def __del__(self):
        """Cleanup on object destruction"""
        self.close_connection()

# Global instance
db_connection = DatabaseConnection()
