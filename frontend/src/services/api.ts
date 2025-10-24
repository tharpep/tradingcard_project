// API service for interacting with the backend
const API_BASE_URL = 'http://localhost:8000';

// Auth token management
let authToken: string | null = null;

export const setAuthToken = (token: string) => {
  authToken = token;
  localStorage.setItem('authToken', token);
};

export const getAuthToken = () => {
  if (!authToken) {
    authToken = localStorage.getItem('authToken');
  }
  return authToken;
};

export const clearAuthToken = () => {
  authToken = null;
  localStorage.removeItem('authToken');
};

// Helper function to get headers with auth
const getHeaders = () => {
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  };
  
  const token = getAuthToken();
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }
  
  return headers;
};

// Types for our card data
export interface Card {
  id: string; // Changed from number to string for UUID support
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

// Authentication types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface SignupRequest {
  email: string;
  password: string;
  username: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: {
    id: string;
    email: string;
    username?: string;
  };
}

// API service functions
export const api = {
  // Authentication endpoints
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/signin`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials)
    });
    
    if (!response.ok) {
      let errorMessage = 'Login failed';
      try {
        const error = await response.json();
        errorMessage = error.detail || error.message || 'Login failed';
      } catch (e) {
        errorMessage = `HTTP ${response.status}: ${response.statusText}`;
      }
      throw new Error(errorMessage);
    }
    
    const data = await response.json();
    setAuthToken(data.access_token);
    return data;
  },

  async signup(userData: SignupRequest): Promise<AuthResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/signup`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    
    if (!response.ok) {
      let errorMessage = 'Signup failed';
      try {
        const error = await response.json();
        // Handle specific Supabase errors
        if (error.message && error.message.includes('duplicate key')) {
          errorMessage = 'Email already exists. Please try logging in instead.';
        } else if (error.message && error.message.includes('already registered')) {
          errorMessage = 'This email is already registered. Please try logging in.';
        } else {
          errorMessage = error.detail || error.message || 'Signup failed';
        }
      } catch (e) {
        errorMessage = `HTTP ${response.status}: ${response.statusText}`;
      }
      throw new Error(errorMessage);
    }
    
    const data = await response.json();
    setAuthToken(data.access_token);
    return data;
  },

  async logout(): Promise<void> {
    try {
      await fetch(`${API_BASE_URL}/auth/signout`, {
        method: 'POST',
        headers: getHeaders()
      });
    } finally {
      clearAuthToken();
    }
  },

  async getCurrentUser(): Promise<AuthResponse['user']> {
    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      headers: getHeaders()
    });
    
    if (!response.ok) {
      throw new Error('Failed to get current user');
    }
    
    return response.json();
  },
  // Get all cards
  async getCards(): Promise<Card[]> {
    const response = await fetch(`${API_BASE_URL}/cards`, {
      headers: getHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch cards');
    const data = await response.json();
    return data.cards;
  },

  // Get a specific card
  async getCard(id: string): Promise<Card> {
    const response = await fetch(`${API_BASE_URL}/cards/${id}`, {
      headers: getHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch card');
    return response.json();
  },

  // Add a new card
  async addCard(card: CardCreate): Promise<Card> {
    const response = await fetch(`${API_BASE_URL}/cards`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(card)
    });
    if (!response.ok) throw new Error('Failed to add card');
    return response.json();
  },

  // Update a card
  async updateCard(id: string, updates: CardUpdate): Promise<Card> {
    const response = await fetch(`${API_BASE_URL}/cards/${id}`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify(updates)
    });
    if (!response.ok) throw new Error('Failed to update card');
    return response.json();
  },

  // Delete a card
  async deleteCard(id: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/cards/${id}`, {
      method: 'DELETE',
      headers: getHeaders()
    });
    if (!response.ok) throw new Error('Failed to delete card');
  },

  // Search cards by name
  async searchCards(name: string): Promise<Card[]> {
    const response = await fetch(`${API_BASE_URL}/cards/search?name=${encodeURIComponent(name)}`, {
      headers: getHeaders()
    });
    if (!response.ok) throw new Error('Failed to search cards');
    const data = await response.json();
    return data.cards;
  },

  // Get favorite cards
  async getFavorites(): Promise<Card[]> {
    const response = await fetch(`${API_BASE_URL}/cards/favorites`, {
      headers: getHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch favorites');
    const data = await response.json();
    return data.cards;
  },

  // Get collection statistics
  async getStats(): Promise<{ total_cards: number; total_quantity: number; favorite_count: number }> {
    const response = await fetch(`${API_BASE_URL}/cards/stats`, {
      headers: getHeaders()
    });
    if (!response.ok) throw new Error('Failed to fetch stats');
    return response.json();
  }
};
