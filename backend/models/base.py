from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BaseModelWithTimestamps(BaseModel):
    """Base model with common timestamp functionality"""
    
    def to_dict(self) -> dict:
        """Convert model to dictionary"""
        return self.model_dump()
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create model from dictionary"""
        return cls(**data)
