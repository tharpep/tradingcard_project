-- Sample Card Data for Development
-- This inserts sample trading cards for testing

-- Insert sample Pokemon cards
INSERT INTO cards (name, set_name, card_number, rarity, quantity, is_favorite, card_grade, card_price, card_type, notes, tags) VALUES
('Charizard', 'Base Set', '4', 'Rare Holo', 1, TRUE, 9.5, 150.00, 'Pokemon', 'My favorite card from childhood', ARRAY['starter', 'fire', 'rare']),
('Pikachu', 'Base Set', '58', 'Common', 3, FALSE, 7.0, 5.00, 'Pokemon', 'Multiple copies for trading', ARRAY['electric', 'common', 'starter']),
('Blastoise', 'Base Set', '2', 'Rare Holo', 1, TRUE, 8.5, 75.00, 'Pokemon', 'Great condition, slight edge wear', ARRAY['water', 'rare', 'starter']),
('Venusaur', 'Base Set', '15', 'Rare Holo', 1, FALSE, 6.0, 45.00, 'Pokemon', 'Some corner damage', ARRAY['grass', 'rare', 'starter']),
('Mewtwo', 'Base Set', '10', 'Rare Holo', 1, TRUE, 9.0, 120.00, 'Pokemon', 'Near mint condition', ARRAY['psychic', 'rare', 'legendary']),
('Alakazam', 'Base Set', '1', 'Rare Holo', 1, FALSE, 7.5, 35.00, 'Pokemon', 'Good condition overall', ARRAY['psychic', 'rare']),
('Machamp', 'Base Set', '8', 'Rare Holo', 1, FALSE, 6.5, 25.00, 'Pokemon', 'Some surface scratches', ARRAY['fighting', 'rare']),
('Zapdos', 'Base Set', '16', 'Rare Holo', 1, TRUE, 8.0, 60.00, 'Pokemon', 'Excellent condition', ARRAY['electric', 'rare', 'legendary']),
('Dragonite', 'Base Set', '4', 'Rare Holo', 1, FALSE, 7.0, 40.00, 'Pokemon', 'Minor edge wear', ARRAY['dragon', 'rare']),
('Gyarados', 'Base Set', '6', 'Rare Holo', 1, FALSE, 8.5, 55.00, 'Pokemon', 'Very good condition', ARRAY['water', 'rare']);

-- Insert sample Magic: The Gathering cards
INSERT INTO cards (name, set_name, card_number, rarity, quantity, is_favorite, card_grade, card_price, card_type, notes, tags) VALUES
('Black Lotus', 'Alpha', '1', 'Rare', 1, TRUE, 9.5, 50000.00, 'Magic', 'The holy grail of Magic cards', ARRAY['power9', 'artifact', 'rare']),
('Lightning Bolt', 'Alpha', '161', 'Common', 4, FALSE, 8.0, 200.00, 'Magic', 'Classic red spell', ARRAY['instant', 'red', 'common']),
('Ancestral Recall', 'Alpha', '1', 'Rare', 1, TRUE, 9.0, 15000.00, 'Magic', 'Power 9 card', ARRAY['power9', 'blue', 'rare']),
('Time Walk', 'Alpha', '1', 'Rare', 1, TRUE, 8.5, 8000.00, 'Magic', 'Another Power 9', ARRAY['power9', 'blue', 'rare']),
('Mox Pearl', 'Alpha', '1', 'Rare', 1, FALSE, 7.5, 3000.00, 'Magic', 'White Mox', ARRAY['power9', 'artifact', 'rare']),
('Mox Sapphire', 'Alpha', '1', 'Rare', 1, FALSE, 8.0, 3500.00, 'Magic', 'Blue Mox', ARRAY['power9', 'artifact', 'rare']),
('Mox Jet', 'Alpha', '1', 'Rare', 1, FALSE, 7.0, 2500.00, 'Magic', 'Black Mox', ARRAY['power9', 'artifact', 'rare']),
('Mox Ruby', 'Alpha', '1', 'Rare', 1, FALSE, 8.5, 4000.00, 'Magic', 'Red Mox', ARRAY['power9', 'artifact', 'rare']),
('Mox Emerald', 'Alpha', '1', 'Rare', 1, FALSE, 7.5, 2800.00, 'Magic', 'Green Mox', ARRAY['power9', 'artifact', 'rare']),
('Sol Ring', 'Alpha', '1', 'Uncommon', 2, FALSE, 8.0, 500.00, 'Magic', 'Great mana acceleration', ARRAY['artifact', 'uncommon']);

-- Insert sample Yu-Gi-Oh! cards
INSERT INTO cards (name, set_name, card_number, rarity, quantity, is_favorite, card_grade, card_price, card_type, notes, tags) VALUES
('Blue-Eyes White Dragon', 'Legend of Blue Eyes', 'LOB-001', 'Ultra Rare', 1, TRUE, 9.0, 800.00, 'Yu-Gi-Oh', 'Iconic dragon card', ARRAY['dragon', 'ultra', 'rare']),
('Dark Magician', 'Magic Ruler', 'MRD-000', 'Ultra Rare', 1, TRUE, 8.5, 600.00, 'Yu-Gi-Oh', 'Classic spellcaster', ARRAY['spellcaster', 'ultra', 'rare']),
('Red-Eyes B. Dragon', 'Legend of Blue Eyes', 'LOB-005', 'Ultra Rare', 1, FALSE, 7.5, 300.00, 'Yu-Gi-Oh', 'Good condition dragon', ARRAY['dragon', 'ultra', 'rare']),
('Exodia the Forbidden One', 'Legend of Blue Eyes', 'LOB-124', 'Ultra Rare', 1, TRUE, 9.5, 2000.00, 'Yu-Gi-Oh', 'Complete Exodia set', ARRAY['spellcaster', 'ultra', 'rare', 'exodia']),
('Right Arm of the Forbidden One', 'Legend of Blue Eyes', 'LOB-125', 'Common', 1, FALSE, 8.0, 50.00, 'Yu-Gi-Oh', 'Exodia piece', ARRAY['spellcaster', 'common', 'exodia']),
('Left Arm of the Forbidden One', 'Legend of Blue Eyes', 'LOB-126', 'Common', 1, FALSE, 7.5, 45.00, 'Yu-Gi-Oh', 'Exodia piece', ARRAY['spellcaster', 'common', 'exodia']),
('Right Leg of the Forbidden One', 'Legend of Blue Eyes', 'LOB-127', 'Common', 1, FALSE, 8.5, 55.00, 'Yu-Gi-Oh', 'Exodia piece', ARRAY['spellcaster', 'common', 'exodia']),
('Left Leg of the Forbidden One', 'Legend of Blue Eyes', 'LOB-128', 'Common', 1, FALSE, 7.0, 40.00, 'Yu-Gi-Oh', 'Exodia piece', ARRAY['spellcaster', 'common', 'exodia']),
('Kuriboh', 'Legend of Blue Eyes', 'LOB-124', 'Common', 2, FALSE, 6.5, 15.00, 'Yu-Gi-Oh', 'Cute little monster', ARRAY['fiend', 'common']),
('Celtic Guardian', 'Legend of Blue Eyes', 'LOB-125', 'Common', 1, FALSE, 7.0, 20.00, 'Yu-Gi-Oh', 'Warrior monster', ARRAY['warrior', 'common']);
