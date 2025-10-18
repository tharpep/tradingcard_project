from typing import List, Dict, Any, Optional
import logging
from .base_repository import BaseRepository
from database.connection import db_connection
from database.schema import create_tables

logger = logging.getLogger(__name__)

class CardRepository(BaseRepository):
    """Repository for card database operations"""
    
    def __init__(self):
        super().__init__("cards")
        # Ensure tables exist on first use
        create_tables()
    
    def create(self, data: Dict[str, Any]) -> int:
        """Create a new card and return its ID"""
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        
        # Prepare SQL with placeholders
        columns = list(data.keys())
        placeholders = ', '.join(['?' for _ in columns])
        column_names = ', '.join(columns)
        
        sql = f"INSERT INTO {self.table_name} ({column_names}) VALUES ({placeholders})"
        values = list(data.values())
        
        logger.info(f"Creating card: {data.get('name', 'Unknown')}")
        cursor.execute(sql, values)
        conn.commit()
        
        card_id = cursor.lastrowid
        logger.info(f"Card created with ID: {card_id}")
        return card_id
    
    def find_by_id(self, card_id: int) -> Optional[Dict[str, Any]]:
        """Find a card by ID"""
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = ?", (card_id,))
        row = cursor.fetchone()
        
        if row:
            return dict(row)
        return None
    
    def find_all(self) -> List[Dict[str, Any]]:
        """Find all cards"""
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT * FROM {self.table_name} ORDER BY date_added DESC")
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    def find_by_name(self, name: str) -> List[Dict[str, Any]]:
        """Search cards by name (partial match)"""
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            f"SELECT * FROM {self.table_name} WHERE name LIKE ? ORDER BY name",
            (f"%{name}%",)
        )
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    def find_favorites(self) -> List[Dict[str, Any]]:
        """Find all favorite cards"""
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            f"SELECT * FROM {self.table_name} WHERE is_favorite = 1 ORDER BY name"
        )
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]
    
    def update(self, card_id: int, data: Dict[str, Any]) -> bool:
        """Update a card by ID"""
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        
        # Build dynamic UPDATE query
        set_clauses = []
        values = []
        
        for key, value in data.items():
            set_clauses.append(f"{key} = ?")
            values.append(value)
        
        if not set_clauses:
            logger.warning("No fields to update")
            return False
        
        values.append(card_id)
        sql = f"UPDATE {self.table_name} SET {', '.join(set_clauses)} WHERE id = ?"
        
        logger.info(f"Updating card ID {card_id}: {list(data.keys())}")
        cursor.execute(sql, values)
        conn.commit()
        
        return cursor.rowcount > 0
    
    def delete(self, card_id: int) -> bool:
        """Delete a card by ID"""
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        
        logger.info(f"Deleting card ID: {card_id}")
        cursor.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (card_id,))
        conn.commit()
        
        return cursor.rowcount > 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get collection statistics"""
        conn = db_connection.get_connection()
        cursor = conn.cursor()
        
        # Total cards
        cursor.execute(f"SELECT COUNT(*) as total_cards FROM {self.table_name}")
        total_cards = cursor.fetchone()['total_cards']
        
        # Total quantity
        cursor.execute(f"SELECT SUM(quantity) as total_quantity FROM {self.table_name}")
        total_quantity = cursor.fetchone()['total_quantity'] or 0
        
        # Favorites count
        cursor.execute(f"SELECT COUNT(*) as favorites FROM {self.table_name} WHERE is_favorite = 1")
        favorites = cursor.fetchone()['favorites']
        
        # Most common set
        cursor.execute(f"""
            SELECT set_name, COUNT(*) as count 
            FROM {self.table_name} 
            GROUP BY set_name 
            ORDER BY count DESC 
            LIMIT 1
        """)
        most_common_set = cursor.fetchone()
        
        return {
            'total_cards': total_cards,
            'total_quantity': total_quantity,
            'favorites': favorites,
            'most_common_set': most_common_set['set_name'] if most_common_set else 'None'
        }
