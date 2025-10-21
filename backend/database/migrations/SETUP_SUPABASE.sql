-- ============================================================================
-- SUPABASE INITIAL SETUP - Trading Card Collection
-- ============================================================================
-- This script sets up the complete database schema for the trading card app
-- Safe to run multiple times (uses IF NOT EXISTS checks)
-- 
-- Usage: Copy this entire file and paste into Supabase SQL Editor, then Run
-- ============================================================================

-- Enable UUID extension for unique IDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- CARDS TABLE
-- ============================================================================
-- Stores individual trading cards with all metadata
-- Handles duplicate prevention via unique constraint + quantity increment

CREATE TABLE IF NOT EXISTS cards (
    -- Core identification
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    set_name VARCHAR(255) DEFAULT 'Unknown',
    card_number VARCHAR(50),
    rarity VARCHAR(100),
    
    -- Quantity and favorites
    quantity INTEGER DEFAULT 1 CHECK (quantity > 0),
    is_favorite BOOLEAN DEFAULT FALSE,
    
    -- Condition and pricing
    card_grade DECIMAL(3,1) DEFAULT 5.0 CHECK (card_grade >= 0 AND card_grade <= 10),
    card_price DECIMAL(10,2) DEFAULT 0.00 CHECK (card_price >= 0),
    
    -- Classification and metadata
    card_type VARCHAR(50) DEFAULT 'Unknown',
    notes TEXT DEFAULT NULL,
    image_url VARCHAR(500) DEFAULT NULL,
    last_updated_price TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    tags TEXT[] DEFAULT ARRAY[]::TEXT[],
    
    -- User ownership (for future authentication)
    user_id UUID DEFAULT NULL,
    
    -- Timestamps
    date_added TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Unique constraint: prevent duplicate cards (same name, set, number per user)
    CONSTRAINT unique_card_per_user UNIQUE (name, set_name, card_number, user_id)
);

-- ============================================================================
-- INDEXES - Performance Optimization
-- ============================================================================

-- Single-column indexes for common queries
CREATE INDEX IF NOT EXISTS idx_cards_name ON cards(name);
CREATE INDEX IF NOT EXISTS idx_cards_set_name ON cards(set_name);
CREATE INDEX IF NOT EXISTS idx_cards_rarity ON cards(rarity);
CREATE INDEX IF NOT EXISTS idx_cards_is_favorite ON cards(is_favorite);
CREATE INDEX IF NOT EXISTS idx_cards_date_added ON cards(date_added);
CREATE INDEX IF NOT EXISTS idx_cards_grade ON cards(card_grade);
CREATE INDEX IF NOT EXISTS idx_cards_price ON cards(card_price);
CREATE INDEX IF NOT EXISTS idx_cards_user_id ON cards(user_id);
CREATE INDEX IF NOT EXISTS idx_cards_type ON cards(card_type);
CREATE INDEX IF NOT EXISTS idx_cards_last_updated_price ON cards(last_updated_price);

-- Composite indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_cards_user_type ON cards(user_id, card_type) WHERE user_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_cards_user_favorite ON cards(user_id, is_favorite) WHERE user_id IS NOT NULL AND is_favorite = TRUE;
CREATE INDEX IF NOT EXISTS idx_cards_type_price ON cards(card_type, card_price DESC);

-- GIN index for tag array searching
CREATE INDEX IF NOT EXISTS idx_cards_tags ON cards USING GIN(tags);

-- ============================================================================
-- TRIGGERS - Automatic Timestamp Updates
-- ============================================================================

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger (drop first to avoid conflicts)
DROP TRIGGER IF EXISTS update_cards_updated_at ON cards;
CREATE TRIGGER update_cards_updated_at 
    BEFORE UPDATE ON cards 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- HELPER FUNCTIONS - Business Logic
-- ============================================================================

-- Function to add card or increment quantity if duplicate exists
CREATE OR REPLACE FUNCTION add_or_increment_card(
    p_name VARCHAR(255),
    p_set_name VARCHAR(255),
    p_card_number VARCHAR(50),
    p_rarity VARCHAR(100),
    p_quantity INTEGER,
    p_is_favorite BOOLEAN,
    p_card_grade DECIMAL(3,1),
    p_card_price DECIMAL(10,2),
    p_card_type VARCHAR(50),
    p_notes TEXT,
    p_image_url VARCHAR(500),
    p_last_updated_price TIMESTAMP WITH TIME ZONE,
    p_tags TEXT[],
    p_user_id UUID
) RETURNS UUID AS $$
DECLARE
    v_card_id UUID;
BEGIN
    -- Try to insert the card, increment quantity if it already exists
    INSERT INTO cards (
        name, set_name, card_number, rarity, quantity, is_favorite,
        card_grade, card_price, card_type, notes, image_url,
        last_updated_price, tags, user_id
    ) VALUES (
        p_name, p_set_name, p_card_number, p_rarity, p_quantity, p_is_favorite,
        p_card_grade, p_card_price, p_card_type, p_notes, p_image_url,
        p_last_updated_price, p_tags, p_user_id
    )
    ON CONFLICT (name, set_name, card_number, user_id)
    DO UPDATE SET
        quantity = cards.quantity + p_quantity,
        updated_at = NOW()
    RETURNING id INTO v_card_id;
    
    RETURN v_card_id;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- DOCUMENTATION - SQL Comments
-- ============================================================================

COMMENT ON TABLE cards IS 'Stores trading card collection data';
COMMENT ON FUNCTION add_or_increment_card IS 'Add new card or increment quantity if duplicate exists';

COMMENT ON COLUMN cards.id IS 'Unique identifier for each card';
COMMENT ON COLUMN cards.name IS 'Name of the trading card';
COMMENT ON COLUMN cards.set_name IS 'Name of the card set/series';
COMMENT ON COLUMN cards.card_number IS 'Card number within the set';
COMMENT ON COLUMN cards.rarity IS 'Card rarity (Common, Uncommon, Rare, etc.)';
COMMENT ON COLUMN cards.quantity IS 'Number of copies owned';
COMMENT ON COLUMN cards.is_favorite IS 'Whether this card is marked as favorite';
COMMENT ON COLUMN cards.card_grade IS 'Card condition grade (0.0-10.0, default 5.0)';
COMMENT ON COLUMN cards.card_price IS 'Card value/price (default 0.00)';
COMMENT ON COLUMN cards.card_type IS 'Type of card (Pokemon, Magic, Yu-Gi-Oh, etc.)';
COMMENT ON COLUMN cards.notes IS 'Personal notes about the card';
COMMENT ON COLUMN cards.image_url IS 'URL to card image';
COMMENT ON COLUMN cards.last_updated_price IS 'When price was last updated';
COMMENT ON COLUMN cards.tags IS 'Array of tags for organization and searching';
COMMENT ON COLUMN cards.user_id IS 'Owner of this card (NULL for anonymous)';
COMMENT ON COLUMN cards.date_added IS 'When this card was added to collection';

-- ============================================================================
-- SETUP COMPLETE!
-- ============================================================================
-- Next steps:
-- 1. Verify the 'cards' table appears in your Supabase Table Editor
-- 2. Optionally run seeds/sample_cards.sql to add test data
-- 3. Update your backend to use Supabase instead of SQLite
-- ============================================================================

