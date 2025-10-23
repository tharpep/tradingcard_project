"""
User-facing CLI commands for card management
"""

import sys
from services.card_service import CardService

def handle_user_command(command: str, args: list, card_service: CardService):
    """Route user commands to appropriate handlers"""
    if command == "add":
        add_card(card_service, args)
    elif command == "list":
        list_cards(card_service, args)
    elif command == "search":
        search_cards(card_service, args)
    elif command == "delete":
        delete_card(card_service, args)
    elif command == "update":
        update_card(card_service, args)
    elif command == "stats":
        show_stats(card_service, args)

def add_card(card_service: CardService, args: list):
    """Add a new card to your collection"""
    if len(args) < 1:
        print("Usage: python run add <name> [--set <set>] [--number <number>] [--rarity <rarity>] [--quantity <qty>] [--favorite] [--no-validate]")
        return
    
    # Admin CLI - No authentication needed
    
    name = args[0]
    set_name = "Unknown"
    card_number = None
    rarity = None
    quantity = 1
    favorite = False
    validate_pokemon = True
    
    # Parse options
    i = 1
    while i < len(args):
        if args[i] == "--set" and i + 1 < len(args):
            set_name = args[i + 1]
            i += 2
        elif args[i] == "--number" and i + 1 < len(args):
            card_number = args[i + 1]
            i += 2
        elif args[i] == "--rarity" and i + 1 < len(args):
            rarity = args[i + 1]
            i += 2
        elif args[i] == "--quantity" and i + 1 < len(args):
            quantity = int(args[i + 1])
            i += 2
        elif args[i] == "--favorite":
            favorite = True
            i += 1
        elif args[i] == "--no-validate":
            validate_pokemon = False
            i += 1
        else:
            i += 1
    
    try:
        if validate_pokemon:
            print(f"Adding Pokemon card: {name}")
            print("Note: Pokemon validation is currently disabled due to API reliability issues")
        
        # Using global admin card_service
        card_id = card_service.add_card(
            name=name,
            set_name=set_name,
            card_number=card_number,
            rarity=rarity,
            quantity=quantity,
            is_favorite=favorite,
            validate_pokemon=validate_pokemon
        )
        
        print(f"Card added successfully with ID: {card_id}")
        print(f"   Name: {name}")
        print(f"   Set: {set_name}")
        if card_number:
            print(f"   Number: {card_number}")
        if rarity:
            print(f"   Rarity: {rarity}")
        print(f"   Quantity: {quantity}")
        if favorite:
            print("   Marked as favorite")
            
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def list_cards(card_service: CardService, args: list):
    """List all cards in your collection"""
    # Admin CLI - No authentication needed
    
    favorites_only = "--favorites" in args or "-f" in args
    
    try:
        # Using global admin card_service
        if favorites_only:
            cards = card_service.get_favorites()
            if not cards:
                print("No favorite cards found")
                return
        else:
            cards = card_service.get_all_cards()
            if not cards:
                print("Your collection is empty")
                return
        
        # Prepare table data
        headers = ["ID", "Name", "Set", "Number", "Rarity", "Qty", "Favorite", "Added"]
        table_data = []
        
        for card in cards:
            table_data.append([
                card['id'],
                card['name'],
                card['set_name'],
                card['card_number'] or '-',
                card['rarity'] or '-',
                card['quantity'],
                '*' if card['is_favorite'] else '',
                card['date_added'][:10]  # Just the date part
            ])
        
        # Simple table output
        print(f"{'ID':<4} {'Name':<20} {'Set':<15} {'Number':<8} {'Rarity':<12} {'Qty':<3} {'Fav':<3} {'Added':<10}")
        print("-" * 80)
        for row in table_data:
            print(f"{row[0]:<4} {row[1]:<20} {row[2]:<15} {row[3]:<8} {row[4]:<12} {row[5]:<3} {row[6]:<3} {row[7]:<10}")
        
        if favorites_only:
            print(f"\nShowing {len(cards)} favorite cards")
        else:
            print(f"\nTotal cards: {len(cards)}")
            
    except Exception as e:
        print(f"Error listing cards: {e}")
        sys.exit(1)

def search_cards(card_service: CardService, args: list):
    """Search for cards by name"""
    if len(args) < 1:
        print("Usage: python run search <name>")
        return
    
    # Admin CLI - No authentication needed
    
    name = args[0]
    
    try:
        # Using global admin card_service
        cards = card_service.search_cards(name)
        
        if not cards:
            print(f"No cards found matching '{name}'")
            return
        
        # Prepare table data
        headers = ["ID", "Name", "Set", "Number", "Rarity", "Qty", "Favorite"]
        table_data = []
        
        for card in cards:
            table_data.append([
                card['id'],
                card['name'],
                card['set_name'],
                card['card_number'] or '-',
                card['rarity'] or '-',
                card['quantity'],
                '*' if card['is_favorite'] else ''
            ])
        
        # Simple table output
        print(f"{'ID':<4} {'Name':<20} {'Set':<15} {'Number':<8} {'Rarity':<12} {'Qty':<3} {'Fav':<3} {'Added':<10}")
        print("-" * 80)
        for row in table_data:
            print(f"{row[0]:<4} {row[1]:<20} {row[2]:<15} {row[3]:<8} {row[4]:<12} {row[5]:<3} {row[6]:<3} {row[7]:<10}")
        print(f"\nFound {len(cards)} cards matching '{name}'")
        
    except Exception as e:
        print(f"Error searching cards: {e}")
        sys.exit(1)

def delete_card(card_service: CardService, args: list):
    """Delete a card from your collection"""
    if len(args) < 1:
        print("Usage: python run delete <id>")
        return
    
    # Admin CLI - No authentication needed
    
    try:
        card_id = int(args[0])
    except ValueError:
        print("Error: Card ID must be a number")
        return
    
    try:
        # Using global admin card_service
        # First check if card exists
        card = card_service.get_card(card_id)
        if not card:
            print(f"Card with ID {card_id} not found")
            sys.exit(1)
        
        # Confirm deletion
        print(f"Are you sure you want to delete '{card['name']}'?")
        response = input("This action cannot be undone (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("Deletion cancelled")
            return
        
        success = card_service.delete_card(card_id)
        if success:
            print(f"Card '{card['name']}' deleted successfully")
        else:
            print(f"Failed to delete card {card_id}")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error deleting card: {e}")
        sys.exit(1)

def show_stats(card_service: CardService, args: list):
    """Show collection statistics"""
    try:
        stats = card_service.get_collection_stats()
        
        print("Collection Statistics")
        print("=" * 30)
        print(f"Total Cards: {stats['total_cards']}")
        print(f"Total Quantity: {stats['total_quantity']}")
        print(f"Favorite Cards: {stats['favorites']}")
        print(f"Most Common Set: {stats['most_common_set']}")
        
    except Exception as e:
        print(f"Error getting stats: {e}")
        sys.exit(1)

def update_card(card_service: CardService, args: list):
    """Update a card in your collection"""
    if len(args) < 1:
        print("Usage: python run update <id> [--name <name>] [--set <set>] [--number <number>] [--rarity <rarity>] [--quantity <qty>] [--favorite]")
        return
    
    try:
        card_id = int(args[0])
    except ValueError:
        print("Error: Card ID must be a number")
        return
    
    # Parse update options
    update_data = {}
    i = 1
    while i < len(args):
        if args[i] == "--name" and i + 1 < len(args):
            update_data['name'] = args[i + 1]
            i += 2
        elif args[i] == "--set" and i + 1 < len(args):
            update_data['set_name'] = args[i + 1]
            i += 2
        elif args[i] == "--number" and i + 1 < len(args):
            update_data['card_number'] = args[i + 1]
            i += 2
        elif args[i] == "--rarity" and i + 1 < len(args):
            update_data['rarity'] = args[i + 1]
            i += 2
        elif args[i] == "--quantity" and i + 1 < len(args):
            update_data['quantity'] = int(args[i + 1])
            i += 2
        elif args[i] == "--favorite":
            # Toggle favorite status
            card = card_service.get_card(card_id)
            if card:
                update_data['is_favorite'] = not card['is_favorite']
            i += 1
        else:
            i += 1
    
    if not update_data:
        print("No fields to update. Use --help to see available options.")
        return
    
    try:
        # Check if card exists
        card = card_service.get_card(card_id)
        if not card:
            print(f"Card with ID {card_id} not found")
            sys.exit(1)
        
        success = card_service.update_card(card_id, **update_data)
        if success:
            print(f"Card '{card['name']}' updated successfully")
        else:
            print(f"Failed to update card {card_id}")
            sys.exit(1)
            
    except ValueError as e:
        print(f"Validation error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error updating card: {e}")
        sys.exit(1)
