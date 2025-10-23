"""
Admin routes for CLI access
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from services.card_service import CardService
from api.models.responses import (
    CardResponse, 
    CardListResponse, 
    StatsResponse, 
    MessageResponse,
    ErrorResponse
)
from api.middleware.auth import verify_admin_api_key
import logging
import requests
from config import Config

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users")
async def list_all_users(admin_key: str = Depends(verify_admin_api_key)):
    """List all users in the system - CLI only"""
    try:
        logger.info("Admin request: List all users")
        
        headers = {
            'apikey': Config.SUPABASE_KEY,
            'Authorization': f'Bearer {Config.SUPABASE_KEY}',
            'Content-Type': 'application/json'
        }
        
        # Get all users from Supabase
        response = requests.get(
            f"{Config.SUPABASE_URL}/rest/v1/users",
            headers=headers
        )
        response.raise_for_status()
        users = response.json()
        
        logger.info(f"Retrieved {len(users)} users")
        return {
            "users": users,
            "total": len(users)
        }
        
    except Exception as e:
        logger.error(f"Error listing users: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving users: {str(e)}")

@router.get("/cards/all", response_model=CardListResponse)
async def get_all_cards(admin_key: str = Depends(verify_admin_api_key)):
    """Get ALL cards from ALL users - CLI only"""
    try:
        logger.info("Admin request: Get all cards from all users")
        
        # Admin card service - full system access
        card_service = CardService(admin=True)
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
        
        logger.info(f"Retrieved {len(card_responses)} cards from all users")
        return CardListResponse(cards=card_responses, total=len(card_responses))
        
    except Exception as e:
        logger.error(f"Error retrieving all cards: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving all cards: {str(e)}")

@router.get("/cards/user/{user_id}", response_model=CardListResponse)
async def get_user_cards(user_id: str, admin_key: str = Depends(verify_admin_api_key)):
    """Get cards for a specific user - CLI only"""
    try:
        logger.info(f"Admin request: Get cards for user {user_id}")
        
        # Admin card service - can access any user's data
        card_service = CardService(admin=True)
        
        # Get all cards and filter by user_id
        all_cards = card_service.get_all_cards()
        user_cards = [card for card in all_cards if card.get('user_id') == user_id]
        
        card_responses = [CardResponse(
            id=card['id'],
            name=card['name'],
            set_name=card['set_name'],
            card_number=card.get('card_number'),
            rarity=card.get('rarity'),
            quantity=card['quantity'],
            is_favorite=bool(card['is_favorite']),
            date_added=card['date_added']
        ) for card in user_cards]
        
        logger.info(f"Retrieved {len(card_responses)} cards for user {user_id}")
        return CardListResponse(cards=card_responses, total=len(card_responses))
        
    except Exception as e:
        logger.error(f"Error retrieving cards for user {user_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving user cards: {str(e)}")

@router.get("/stats/all", response_model=StatsResponse)
async def get_system_stats(admin_key: str = Depends(verify_admin_api_key)):
    """Get system-wide statistics - CLI only"""
    try:
        logger.info("Admin request: Get system-wide statistics")
        
        # Admin card service - full system access
        card_service = CardService(admin=True)
        stats = card_service.get_collection_stats()
        
        logger.info(f"Retrieved system stats: {stats}")
        return StatsResponse(**stats)
        
    except Exception as e:
        logger.error(f"Error retrieving system stats: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving system stats: {str(e)}")

@router.delete("/cards/clear")
async def clear_all_cards(admin_key: str = Depends(verify_admin_api_key)):
    """Clear all cards from the system - CLI only"""
    try:
        logger.info("Admin request: Clear all cards")
        
        # Admin card service - full system access
        card_service = CardService(admin=True)
        success = card_service.delete_all_cards()
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to clear all cards")
        
        logger.info("Successfully cleared all cards")
        return {"message": "All cards cleared successfully"}
        
    except Exception as e:
        logger.error(f"Error clearing all cards: {e}")
        raise HTTPException(status_code=500, detail=f"Error clearing cards: {str(e)}")
