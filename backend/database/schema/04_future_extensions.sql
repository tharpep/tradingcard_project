-- Future Schema Extensions
-- This file contains planned schema additions for future features
-- These are NOT implemented yet - just planning for expansion

-- Card Sets table - for organizing cards by set/series
-- CREATE TABLE card_sets (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     name VARCHAR(255) NOT NULL,
--     release_date DATE,
--     description TEXT,
--     created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
-- );

-- Card Categories table - for organizing by type (Pokemon, Magic, etc.)
-- CREATE TABLE card_categories (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     name VARCHAR(100) NOT NULL,
--     description TEXT,
--     created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
-- );

-- Card Images table - for storing card images
-- CREATE TABLE card_images (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     card_id UUID NOT NULL REFERENCES cards(id) ON DELETE CASCADE,
--     image_url VARCHAR(500) NOT NULL,
--     is_primary BOOLEAN DEFAULT FALSE,
--     created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
-- );

-- User Preferences table - for user settings
-- CREATE TABLE user_preferences (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
--     theme VARCHAR(50) DEFAULT 'light',
--     language VARCHAR(10) DEFAULT 'en',
--     notifications_enabled BOOLEAN DEFAULT TRUE,
--     created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
--     updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
-- );

-- Collection Statistics table - for caching user stats
-- CREATE TABLE collection_stats (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
--     total_cards INTEGER DEFAULT 0,
--     total_sets INTEGER DEFAULT 0,
--     favorite_cards INTEGER DEFAULT 0,
--     last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW()
-- );

-- Comments for future reference
COMMENT ON TABLE card_sets IS 'Card sets/series information (future feature)';
COMMENT ON TABLE card_categories IS 'Card categories/types (future feature)';
COMMENT ON TABLE card_images IS 'Card image storage (future feature)';
COMMENT ON TABLE user_preferences IS 'User settings and preferences (future feature)';
COMMENT ON TABLE collection_stats IS 'Cached collection statistics (future feature)';
