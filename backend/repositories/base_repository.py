from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Union
import logging

logger = logging.getLogger(__name__)

class BaseRepository(ABC):
    """Abstract base repository for database operations"""
    
    def __init__(self, table_name: str):
        self.table_name = table_name
    
    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Union[int, str]:
        """Create a new record and return its ID"""
        pass
    
    @abstractmethod
    def find_by_id(self, record_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Find a record by ID"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Dict[str, Any]]:
        """Find all records"""
        pass
    
    @abstractmethod
    def update(self, record_id: Union[int, str], data: Dict[str, Any]) -> bool:
        """Update a record by ID"""
        pass
    
    @abstractmethod
    def delete(self, record_id: Union[int, str]) -> bool:
        """Delete a record by ID"""
        pass
    
    def exists(self, record_id: Union[int, str]) -> bool:
        """Check if a record exists by ID"""
        return self.find_by_id(record_id) is not None
