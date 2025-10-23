"""
Admin CLI commands for system management
"""

import sys
import requests
from services.card_service import CardService
from config import Config

def handle_admin_command(command: str, args: list, card_service: CardService):
    """Route admin commands to appropriate handlers"""
    if command == "users":
        list_all_users(args)
    elif command == "cards":
        if len(args) > 0 and args[0] == "all":
            show_all_cards(args[1:], card_service)
        elif len(args) > 1 and args[0] == "user":
            show_user_cards(args[1:], card_service)
        else:
            print("Usage: python run cards all | python run cards user <user_id>")
    elif command == "stats" and len(args) > 0 and args[0] == "all":
        show_system_stats(args[1:], card_service)

def list_all_users(args):
    """List all users in the system"""
    print("👥 All Users")
    print("=" * 30)
    
    try:
        import requests
        from config import Config
        
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
        
        if not users:
            print("No users found")
            return
        
        print(f"Found {len(users)} users:")
        print()
        
        for user in users:
            print(f"ID: {user['id']}")
            print(f"Username: {user['username']}")
            print(f"Email: {user['email']}")
            print(f"Created: {user['created_at']}")
            print("-" * 30)
            
    except Exception as e:
        print(f"❌ Error listing users: {e}")

def show_user_cards(args, card_service: CardService):
    """Show cards for a specific user"""
    if len(args) < 1:
        print("Usage: python run cards user <user_id>")
        return
    
    user_id = args[0]
    print(f"🃏 Cards for User: {user_id}")
    print("=" * 40)
    
    try:
        # Get cards for specific user
        cards = card_service.get_all_cards()
        user_cards = [card for card in cards if card.get('user_id') == user_id]
        
        if not user_cards:
            print(f"No cards found for user {user_id}")
            return
        
        print(f"Found {len(user_cards)} cards:")
        print()
        
        for card in user_cards:
            print(f"ID: {card['id']}")
            print(f"Name: {card['name']}")
            print(f"Set: {card['set_name']}")
            print(f"Quantity: {card['quantity']}")
            print(f"Favorite: {'Yes' if card.get('is_favorite') else 'No'}")
            print("-" * 30)
            
    except Exception as e:
        print(f"❌ Error getting user cards: {e}")

def show_all_cards(args, card_service: CardService):
    """Show ALL cards from ALL users"""
    print("🃏 ALL Cards (Admin View)")
    print("=" * 40)
    
    try:
        cards = card_service.get_all_cards()
        
        if not cards:
            print("No cards found in the system")
            return
        
        print(f"Found {len(cards)} cards total:")
        print()
        
        # Group by user
        user_cards = {}
        for card in cards:
            user_id = card.get('user_id', 'Anonymous')
            if user_id not in user_cards:
                user_cards[user_id] = []
            user_cards[user_id].append(card)
        
        for user_id, user_card_list in user_cards.items():
            print(f"👤 User: {user_id} ({len(user_card_list)} cards)")
            for card in user_card_list:
                print(f"  • {card['name']} ({card['set_name']}) - Qty: {card['quantity']}")
            print()
            
    except Exception as e:
        print(f"❌ Error getting all cards: {e}")

def show_system_stats(args, card_service: CardService):
    """Show system-wide statistics"""
    print("📊 System Statistics")
    print("=" * 30)
    
    try:
        # Get all cards
        cards = card_service.get_all_cards()
        
        if not cards:
            print("No data in the system")
            return
        
        # Calculate stats
        total_cards = len(cards)
        total_quantity = sum(card.get('quantity', 1) for card in cards)
        favorites = sum(1 for card in cards if card.get('is_favorite'))
        
        # Group by user
        user_stats = {}
        for card in cards:
            user_id = card.get('user_id', 'Anonymous')
            if user_id not in user_stats:
                user_stats[user_id] = {'cards': 0, 'quantity': 0, 'favorites': 0}
            user_stats[user_id]['cards'] += 1
            user_stats[user_id]['quantity'] += card.get('quantity', 1)
            if card.get('is_favorite'):
                user_stats[user_id]['favorites'] += 1
        
        print(f"Total Cards: {total_cards}")
        print(f"Total Quantity: {total_quantity}")
        print(f"Total Favorites: {favorites}")
        print(f"Active Users: {len(user_stats)}")
        print()
        
        print("Per User Breakdown:")
        for user_id, stats in user_stats.items():
            print(f"  {user_id}: {stats['cards']} cards, {stats['quantity']} total, {stats['favorites']} favorites")
            
    except Exception as e:
        print(f"❌ Error getting system stats: {e}")
