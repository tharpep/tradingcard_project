from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from services.card_service import CardService
from models.card import CardCreate, CardUpdate
from api.models.responses import (
    CardResponse, 
    CardListResponse, 
    StatsResponse, 
    MessageResponse,
    ErrorResponse
)

router = APIRouter(prefix="/cards", tags=["cards"])

# Initialize card service
card_service = CardService()

@router.get("/", response_model=CardListResponse)
async def get_cards():
    """Get all cards in the collection"""
    try:
        cards = card_service.get_all_cards()
        card_responses = [CardResponse(
            id=card['id'],
            name=card['name'],
            set_name=card['set_name'],
            card_number=card.get('card_number'),
            rarity=card.get('rarity'),
            quantity=card['quantity'],
            is_favorite=bool(card['is_favorite']),
            date_added=card['date_added']
        ) for card in cards]
        return CardListResponse(cards=card_responses, total=len(card_responses))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving cards: {str(e)}")

@router.get("/search", response_model=CardListResponse)
async def search_cards(name: str = Query(..., description="Name to search for")):
    """Search cards by name"""
    try:
        cards = card_service.search_cards(name)
        card_responses = [CardResponse(
            id=card['id'],
            name=card['name'],
            set_name=card['set_name'],
            card_number=card.get('card_number'),
            rarity=card.get('rarity'),
            quantity=card['quantity'],
            is_favorite=bool(card['is_favorite']),
            date_added=card['date_added']
        ) for card in cards]
        return CardListResponse(cards=card_responses, total=len(card_responses))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching cards: {str(e)}")

@router.get("/favorites", response_model=CardListResponse)
async def get_favorites():
    """Get all favorite cards"""
    try:
        cards = card_service.get_favorites()
        card_responses = [CardResponse(
            id=card['id'],
            name=card['name'],
            set_name=card['set_name'],
            card_number=card.get('card_number'),
            rarity=card.get('rarity'),
            quantity=card['quantity'],
            is_favorite=bool(card['is_favorite']),
            date_added=card['date_added']
        ) for card in cards]
        return CardListResponse(cards=card_responses, total=len(card_responses))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving favorites: {str(e)}")

@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get collection statistics"""
    try:
        stats = card_service.get_collection_stats()
        return StatsResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving stats: {str(e)}")

@router.get("/{card_id}", response_model=CardResponse)
async def get_card(card_id: int):
    """Get a specific card by ID"""
    try:
        card = card_service.get_card(card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")
        return CardResponse(
            id=card['id'],
            name=card['name'],
            set_name=card['set_name'],
            card_number=card.get('card_number'),
            rarity=card.get('rarity'),
            quantity=card['quantity'],
            is_favorite=bool(card['is_favorite']),
            date_added=card['date_added']
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving card: {str(e)}")

@router.post("/", response_model=CardResponse)
async def create_card(card_data: CardCreate):
    """Add a new card to the collection"""
    try:
        card_id = card_service.add_card(
            name=card_data.name,
            set_name=card_data.set_name,
            card_number=card_data.card_number,
            rarity=card_data.rarity,
            quantity=card_data.quantity,
            is_favorite=card_data.is_favorite
        )
        
        # Get the created card to return
        card = card_service.get_card(card_id)
        if not card:
            raise HTTPException(status_code=500, detail="Card was created but could not be retrieved")
        return CardResponse(
            id=card['id'],
            name=card['name'],
            set_name=card['set_name'],
            card_number=card.get('card_number'),
            rarity=card.get('rarity'),
            quantity=card['quantity'],
            is_favorite=bool(card['is_favorite']),
            date_added=card['date_added']
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating card: {str(e)}")

@router.put("/{card_id}", response_model=CardResponse)
async def update_card(card_id: int, card_data: CardUpdate):
    """Update an existing card"""
    try:
        # Check if card exists
        existing_card = card_service.get_card(card_id)
        if not existing_card:
            raise HTTPException(status_code=404, detail="Card not found")
        
        # Prepare update data (only include non-None fields)
        update_data = {}
        if card_data.name is not None:
            update_data['name'] = card_data.name
        if card_data.set_name is not None:
            update_data['set_name'] = card_data.set_name
        if card_data.card_number is not None:
            update_data['card_number'] = card_data.card_number
        if card_data.rarity is not None:
            update_data['rarity'] = card_data.rarity
        if card_data.quantity is not None:
            update_data['quantity'] = card_data.quantity
        if card_data.is_favorite is not None:
            update_data['is_favorite'] = card_data.is_favorite
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        success = card_service.update_card(card_id, **update_data)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update card")
        
        # Get the updated card to return
        card = card_service.get_card(card_id)
        if not card:
            raise HTTPException(status_code=500, detail="Card was updated but could not be retrieved")
        return CardResponse(
            id=card['id'],
            name=card['name'],
            set_name=card['set_name'],
            card_number=card.get('card_number'),
            rarity=card.get('rarity'),
            quantity=card['quantity'],
            is_favorite=bool(card['is_favorite']),
            date_added=card['date_added']
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating card: {str(e)}")

@router.delete("/{card_id}", response_model=MessageResponse)
async def delete_card(card_id: int):
    """Delete a card from the collection"""
    try:
        # Check if card exists
        card = card_service.get_card(card_id)
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")
        
        success = card_service.delete_card(card_id)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to delete card")
        
        return MessageResponse(message=f"Card '{card['name']}' deleted successfully")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting card: {str(e)}")
