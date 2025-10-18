from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .base import BaseModelWithTimestamps

class CardCreate(BaseModel):
    """Model for creating a new card"""
    name: str = Field(min_length=1, max_length=100, description="Card name")
    set_name: str = Field(default="Unknown", max_length=100, description="Set name")
    card_number: Optional[str] = Field(None, max_length=20, description="Card number")
    rarity: Optional[str] = Field(None, max_length=50, description="Card rarity")
    quantity: int = Field(default=1, ge=1, description="Quantity owned")
    is_favorite: bool = Field(default=False, description="Is this a favorite card")

class CardUpdate(BaseModel):
    """Model for updating an existing card"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    set_name: Optional[str] = Field(None, max_length=100)
    card_number: Optional[str] = Field(None, max_length=20)
    rarity: Optional[str] = Field(None, max_length=50)
    quantity: Optional[int] = Field(None, ge=1)
    is_favorite: Optional[bool] = None

class Card(BaseModelWithTimestamps):
    """Complete card model with all fields"""
    id: Optional[int] = None
    name: str = Field(min_length=1, max_length=100)
    set_name: str = Field(default="Unknown", max_length=100)
    card_number: Optional[str] = Field(None, max_length=20)
    rarity: Optional[str] = Field(None, max_length=50)
    quantity: int = Field(default=1, ge=1)
    is_favorite: bool = Field(default=False)
    date_added: str = Field(default_factory=lambda: datetime.now().isoformat())
    
    def to_db_dict(self) -> dict:
        """Convert to dictionary for database insertion"""
        data = self.to_dict()
        # Remove id if None (for new records)
        if data.get('id') is None:
            data.pop('id', None)
        return data
