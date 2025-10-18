// Higher-level service for card operations
import { api } from './api';
import type { Card, CardCreate, CardUpdate } from './api';

export class CardService {
  // Get all cards
  async getAllCards(): Promise<Card[]> {
    return api.getCards();
  }

  // Add a new card with defaults
  async addCard(name: string, options?: Partial<CardCreate>): Promise<Card> {
    const cardData: CardCreate = {
      name,
      set_name: 'Unknown',
      quantity: 1,
      is_favorite: false,
      ...options
    };
    return api.addCard(cardData);
  }

  // Update card
  async updateCard(id: number, updates: CardUpdate): Promise<Card> {
    return api.updateCard(id, updates);
  }

  // Delete card
  async deleteCard(id: number): Promise<void> {
    return api.deleteCard(id);
  }

  // Search cards
  async searchCards(query: string): Promise<Card[]> {
    if (!query.trim()) return this.getAllCards();
    return api.searchCards(query);
  }

  // Get favorites
  async getFavorites(): Promise<Card[]> {
    return api.getFavorites();
  }

  // Toggle favorite status
  async toggleFavorite(id: number, currentStatus: boolean): Promise<Card> {
    return api.updateCard(id, { is_favorite: !currentStatus });
  }

  // Get stats
  async getStats() {
    return api.getStats();
  }
}

// Export a singleton instance
export const cardService = new CardService();
