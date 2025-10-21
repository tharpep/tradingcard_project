from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Union
import logging

logger = logging.getLogger(__name__)

class BaseService(ABC):
    """Abstract base service class for business logic"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def create(self, data: Dict[str, Any]) -> Union[int, str]:
        """Create a new record"""
        pass
    
    @abstractmethod
    def get_by_id(self, record_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Get a record by ID"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all records"""
        pass
    
    @abstractmethod
    def update(self, record_id: Union[int, str], data: Dict[str, Any]) -> bool:
        """Update a record"""
        pass
    
    @abstractmethod
    def delete(self, record_id: Union[int, str]) -> bool:
        """Delete a record"""
        pass
