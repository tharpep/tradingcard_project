from pydantic import BaseModel
from typing import List, Optional, Union
from datetime import datetime

class CardResponse(BaseModel):
    """Response model for card data"""
    id: Union[int, str]
    name: str
    set_name: str
    card_number: Optional[str] = None
    rarity: Optional[str] = None
    quantity: int
    is_favorite: bool
    date_added: str
    
    class Config:
        from_attributes = True

class CardListResponse(BaseModel):
    """Response model for list of cards"""
    cards: List[CardResponse]
    total: int

class StatsResponse(BaseModel):
    """Response model for collection statistics"""
    total_cards: int
    total_quantity: int
    favorites: int
    most_common_set: str

class MessageResponse(BaseModel):
    """Response model for simple messages"""
    message: str
    success: bool = True

class ErrorResponse(BaseModel):
    """Response model for errors"""
    error: str
    detail: Optional[str] = None
