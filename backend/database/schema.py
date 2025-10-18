import sqlite3
import logging
from .connection import db_connection

logger = logging.getLogger(__name__)

def create_tables():
    """Create database tables if they don't exist (lazy initialization)"""
    conn = db_connection.get_connection()
    cursor = conn.cursor()
    
    # Create cards table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            set_name TEXT NOT NULL DEFAULT 'Unknown',
            card_number TEXT,
            rarity TEXT,
            quantity INTEGER DEFAULT 1,
            is_favorite INTEGER DEFAULT 0,
            date_added TEXT NOT NULL
        )
    """)
    
    # Create index on name for faster searches
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_cards_name 
        ON cards(name)
    """)
    
    conn.commit()
    logger.info("Database tables created/verified")

def get_table_info():
    """Get information about the cards table structure"""
    conn = db_connection.get_connection()
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA table_info(cards)")
    columns = cursor.fetchall()
    
    logger.info("Cards table structure:")
    for column in columns:
        logger.info(f"  {column[1]} ({column[2]}) - {'NOT NULL' if column[3] else 'NULL'}")
    
    return columns
