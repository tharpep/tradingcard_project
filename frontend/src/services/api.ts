// API service for interacting with the backend
const API_BASE_URL = 'http://localhost:8000';

// Types for our card data
export interface Card {
  id: number;
  name: string;
  set_name: string;
  card_number?: string;
  rarity?: string;
  quantity: number;
  is_favorite: boolean;
  date_added: string;
}

export interface CardCreate {
  name: string;
  set_name?: string;
  card_number?: string;
  rarity?: string;
  quantity?: number;
  is_favorite?: boolean;
}

export interface CardUpdate {
  name?: string;
  set_name?: string;
  card_number?: string;
  rarity?: string;
  quantity?: number;
  is_favorite?: boolean;
}

// API service functions
export const api = {
  // Get all cards
  async getCards(): Promise<Card[]> {
    const response = await fetch(`${API_BASE_URL}/cards`);
    if (!response.ok) throw new Error('Failed to fetch cards');
    const data = await response.json();
    return data.cards;
  },

  // Get a specific card
  async getCard(id: number): Promise<Card> {
    const response = await fetch(`${API_BASE_URL}/cards/${id}`);
    if (!response.ok) throw new Error('Failed to fetch card');
    return response.json();
  },

  // Add a new card
  async addCard(card: CardCreate): Promise<Card> {
    const response = await fetch(`${API_BASE_URL}/cards`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(card)
    });
    if (!response.ok) throw new Error('Failed to add card');
    return response.json();
  },

  // Update a card
  async updateCard(id: number, updates: CardUpdate): Promise<Card> {
    const response = await fetch(`${API_BASE_URL}/cards/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates)
    });
    if (!response.ok) throw new Error('Failed to update card');
    return response.json();
  },

  // Delete a card
  async deleteCard(id: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/cards/${id}`, {
      method: 'DELETE'
    });
    if (!response.ok) throw new Error('Failed to delete card');
  },

  // Search cards by name
  async searchCards(name: string): Promise<Card[]> {
    const response = await fetch(`${API_BASE_URL}/cards/search?name=${encodeURIComponent(name)}`);
    if (!response.ok) throw new Error('Failed to search cards');
    const data = await response.json();
    return data.cards;
  },

  // Get favorite cards
  async getFavorites(): Promise<Card[]> {
    const response = await fetch(`${API_BASE_URL}/cards/favorites`);
    if (!response.ok) throw new Error('Failed to fetch favorites');
    const data = await response.json();
    return data.cards;
  },

  // Get collection statistics
  async getStats(): Promise<{ total_cards: number; total_quantity: number; favorite_count: number }> {
    const response = await fetch(`${API_BASE_URL}/cards/stats`);
    if (!response.ok) throw new Error('Failed to fetch stats');
    return response.json();
  }
};
